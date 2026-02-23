from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
from sqlalchemy.orm import Session
from src.db.database import get_db
from src.db.models import Document, IntentSpace
from src.services.document_service import validate_file, save_and_parse, reparse_document, delete_document
import datetime

router = APIRouter(prefix="/documents", tags=["documents"])


class DocumentResponse(BaseModel):
    id: int
    filename: str
    format: str
    size_bytes: int
    intent_space_id: int
    intent_space_name: str
    status: str
    chunk_count: int
    access_count: int
    error_message: str | None
    uploaded_at: datetime.datetime
    processed_at: datetime.datetime | None

    model_config = {"from_attributes": True}


def _to_response(doc: Document, db: Session) -> DocumentResponse:
    space = db.query(IntentSpace).filter_by(id=doc.intent_space_id).first()
    return DocumentResponse(
        id=doc.id,
        filename=doc.filename,
        format=doc.format,
        size_bytes=doc.size_bytes,
        intent_space_id=doc.intent_space_id,
        intent_space_name=space.name if space else "Unknown",
        status=doc.status,
        chunk_count=doc.chunk_count,
        access_count=doc.access_count,
        error_message=doc.error_message,
        uploaded_at=doc.uploaded_at,
        processed_at=doc.processed_at,
    )


@router.post("", status_code=201)
async def upload_document(
    file: UploadFile = File(...),
    intent_space_id: int = Form(...),
    db: Session = Depends(get_db),
) -> DocumentResponse:
    content = await file.read()
    try:
        validate_file(file.filename or "upload", len(content), file.content_type or "")
        doc = save_and_parse(content, file.filename or "upload", intent_space_id, db)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    return _to_response(doc, db)


@router.get("")
def list_documents(
    intent_space_id: int | None = None,
    search: str | None = None,
    status: str | None = None,
    db: Session = Depends(get_db),
) -> list[DocumentResponse]:
    q = db.query(Document)
    if intent_space_id:
        q = q.filter_by(intent_space_id=intent_space_id)
    if search:
        q = q.filter(Document.filename.ilike(f"%{search}%"))
    if status:
        q = q.filter_by(status=status)
    docs = q.order_by(Document.uploaded_at.desc()).all()
    return [_to_response(d, db) for d in docs]


@router.get("/{doc_id}")
def get_document(doc_id: int, db: Session = Depends(get_db)) -> DocumentResponse:
    doc = db.query(Document).filter_by(id=doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return _to_response(doc, db)


@router.post("/{doc_id}/reparse")
def reparse(doc_id: int, db: Session = Depends(get_db)) -> DocumentResponse:
    try:
        doc = reparse_document(doc_id, db)
    except ValueError as exc:
        code = 404 if "not found" in str(exc).lower() else 400
        raise HTTPException(status_code=code, detail=str(exc))
    return _to_response(doc, db)


@router.delete("/{doc_id}")
def remove_document(doc_id: int, db: Session = Depends(get_db)) -> dict:
    try:
        delete_document(doc_id, db)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    return {"message": "Document deleted successfully"}
