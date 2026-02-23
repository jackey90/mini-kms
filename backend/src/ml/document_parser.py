import logging
import os
import tempfile

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import Docx2txtLoader, PyPDFLoader

logger = logging.getLogger(__name__)

_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    separators=["\n\n", "\n", ". ", " ", ""],
)


def _extract_tables_from_pdf(file_path: str) -> dict[int, list[list[list[str]]]]:
    """Detect and extract tables from each PDF page using pdfplumber.

    Returns {page_index: [[row, ...], ...]} where each row is a list of cell strings.
    """
    try:
        import pdfplumber
    except ImportError:
        logger.warning("pdfplumber not installed — skipping table extraction")
        return {}

    tables_by_page: dict[int, list[list[list[str]]]] = {}
    with pdfplumber.open(file_path) as pdf:
        for page_idx, page in enumerate(pdf.pages):
            raw_tables = page.extract_tables()
            if not raw_tables:
                continue
            cleaned: list[list[list[str]]] = []
            for table in raw_tables:
                rows = [
                    [(cell or "").strip() for cell in row]
                    for row in table
                    if row
                ]
                if rows:
                    cleaned.append(rows)
            if cleaned:
                tables_by_page[page_idx] = cleaned
    return tables_by_page


def _structure_tables_with_ai(tables: list[list[list[str]]]) -> str:
    """Use OpenAI to convert raw tabular data into clean markdown tables."""
    from openai import OpenAI
    from src.config import settings

    if not tables:
        return ""

    raw_lines: list[str] = []
    for i, table in enumerate(tables, 1):
        raw_lines.append(f"Table {i}:")
        for row in table:
            raw_lines.append(" | ".join(row))
        raw_lines.append("")

    client = OpenAI(api_key=settings.openai_api_key)
    resp = client.chat.completions.create(
        model=settings.openai_chat_model,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a document parser. Convert the raw table data into clean "
                    "markdown tables. Identify header rows vs data rows. Preserve ALL "
                    "numerical values exactly. If the table looks like a salary grid, "
                    "policy table, or financial data, add a brief descriptive label "
                    "above it. Output ONLY the markdown tables, nothing else."
                ),
            },
            {"role": "user", "content": "\n".join(raw_lines)},
        ],
        max_tokens=1000,
        temperature=0,
    )
    return resp.choices[0].message.content.strip()


def parse_document(file_bytes: bytes, filename: str) -> list[str]:
    """Parse PDF or DOCX into text chunks.

    For PDFs, also uses pdfplumber to detect embedded tables and
    OpenAI to restructure them into searchable markdown — solving
    the limitation of pure-text extraction for tabular data such as
    HR salary grids or financial statements.
    """
    ext = filename.rsplit(".", 1)[-1].lower()
    if ext not in ("pdf", "docx"):
        raise ValueError(f"Unsupported file format: {ext}")

    with tempfile.NamedTemporaryFile(suffix=f".{ext}", delete=False) as tmp:
        tmp.write(file_bytes)
        tmp_path = tmp.name

    try:
        if ext == "pdf":
            loader = PyPDFLoader(tmp_path)
        else:
            loader = Docx2txtLoader(tmp_path)

        docs = loader.load()
        full_text = "\n\n".join(d.page_content for d in docs if d.page_content.strip())

        # AI-powered table extraction for PDFs
        if ext == "pdf":
            try:
                tables_by_page = _extract_tables_from_pdf(tmp_path)
                if tables_by_page:
                    all_tables = [
                        t for page_tables in tables_by_page.values() for t in page_tables
                    ]
                    structured = _structure_tables_with_ai(all_tables)
                    if structured:
                        full_text = (
                            f"{full_text}\n\n"
                            f"--- Structured Tables ---\n\n"
                            f"{structured}"
                        )
                        logger.info(
                            "Extracted and structured %d table(s) from %s",
                            len(all_tables),
                            filename,
                        )
            except Exception as exc:
                logger.warning("Table extraction failed for %s: %s", filename, exc)

        if not full_text.strip():
            raise ValueError("Document appears to be empty or could not be parsed")

        chunks = _splitter.split_text(full_text)
        return [c for c in chunks if c.strip()]
    finally:
        os.unlink(tmp_path)
