from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import tempfile
import os


_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    separators=["\n\n", "\n", ". ", " ", ""],
)


def parse_document(file_bytes: bytes, filename: str) -> list[str]:
    """Parse PDF or DOCX bytes into a list of text chunks."""
    ext = filename.rsplit(".", 1)[-1].lower()
    if ext not in ("pdf", "docx"):
        raise ValueError(f"Unsupported file format: {ext}")

    # Write to a temp file since LangChain loaders require file paths
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

        if not full_text.strip():
            raise ValueError("Document appears to be empty or could not be parsed")

        chunks = _splitter.split_text(full_text)
        return [c for c in chunks if c.strip()]
    finally:
        os.unlink(tmp_path)
