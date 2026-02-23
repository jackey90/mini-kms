import datetime
import os
from sqlalchemy.orm import Session

from src.config import settings
from src.db.models import Document, IntentSpace
from src.ml.document_parser import parse_document
from src.ml.embedder import embed_texts
from src.ml.vector_store import vector_store


ALLOWED_EXTENSIONS = {"pdf", "docx"}
ALLOWED_MIME_TYPES = {
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
}


def validate_file(filename: str, size_bytes: int, content_type: str) -> None:
    ext = filename.rsplit(".", 1)[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ValueError(f"Unsupported file type: .{ext}. Only PDF and DOCX are supported.")
    if size_bytes > settings.max_file_size_bytes:
        raise ValueError(f"File too large: {size_bytes} bytes. Maximum is {settings.max_file_size_bytes} bytes.")


def save_and_parse(
    file_bytes: bytes,
    filename: str,
    intent_space_id: int,
    db: Session,
) -> Document:
    """Save file, trigger async parsing, return Document record."""
    # Validate intent space exists
    space = db.query(IntentSpace).filter_by(id=intent_space_id).first()
    if not space:
        raise ValueError(f"Intent space {intent_space_id} not found")

    # Save file to disk
    safe_filename = filename.replace(" ", "_")
    doc = Document(
        filename=filename,
        format=filename.rsplit(".", 1)[-1].lower(),
        size_bytes=len(file_bytes),
        file_path="",  # set after we have the doc ID
        intent_space_id=intent_space_id,
        status="processing",
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)

    file_path = os.path.join(settings.data_dir, "uploads", f"{doc.id}_{safe_filename}")
    doc.file_path = file_path
    db.commit()

    with open(file_path, "wb") as f:
        f.write(file_bytes)

    # Parse and vectorize synchronously (acceptable for MVP; no background task queue)
    try:
        chunks = parse_document(file_bytes, filename)
        embeddings = embed_texts(chunks)
        vector_store.add_document_with_embeddings_stored(
            intent_space_id=intent_space_id,
            chunks=chunks,
            embeddings=embeddings,
            document_id=doc.id,
            filename=filename,
        )
        doc.status = "processed"
        doc.chunk_count = len(chunks)
        doc.processed_at = datetime.datetime.utcnow()
    except Exception as exc:
        doc.status = "error"
        doc.error_message = str(exc)

    db.commit()
    db.refresh(doc)
    return doc


def reparse_document(doc_id: int, db: Session) -> Document:
    """Re-read an existing document from disk, re-parse, and re-index it."""
    doc = db.query(Document).filter_by(id=doc_id).first()
    if not doc:
        raise ValueError(f"Document {doc_id} not found")
    if not doc.file_path or not os.path.exists(doc.file_path):
        raise ValueError("Original file not found on disk — please re-upload")

    # Remove old vectors
    vector_store.remove_document(doc.intent_space_id, doc.id)

    doc.status = "processing"
    db.commit()

    try:
        with open(doc.file_path, "rb") as f:
            file_bytes = f.read()

        chunks = parse_document(file_bytes, doc.filename)
        embeddings = embed_texts(chunks)
        vector_store.add_document_with_embeddings_stored(
            intent_space_id=doc.intent_space_id,
            chunks=chunks,
            embeddings=embeddings,
            document_id=doc.id,
            filename=doc.filename,
        )
        doc.status = "processed"
        doc.chunk_count = len(chunks)
        doc.processed_at = datetime.datetime.utcnow()
        doc.error_message = None
    except Exception as exc:
        doc.status = "error"
        doc.error_message = str(exc)

    db.commit()
    db.refresh(doc)
    return doc


def delete_document(doc_id: int, db: Session) -> None:
    doc = db.query(Document).filter_by(id=doc_id).first()
    if not doc:
        raise ValueError(f"Document {doc_id} not found")

    # Remove vectors from FAISS
    vector_store.remove_document(doc.intent_space_id, doc.id)

    # Remove file from disk
    if doc.file_path and os.path.exists(doc.file_path):
        os.remove(doc.file_path)

    db.delete(doc)
    db.commit()
