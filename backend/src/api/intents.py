import json
import datetime
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from src.db.database import get_db
from src.db.models import IntentSpace
from src.services.intent_service import (
    list_intent_spaces, create_intent_space, update_intent_space,
    delete_intent_space, get_document_count,
)

router = APIRouter(prefix="/intents", tags=["intents"])


class IntentSpaceResponse(BaseModel):
    id: int
    name: str
    description: str
    keywords: list[str]
    document_count: int
    is_default: bool
    created_at: datetime.datetime

    model_config = {"from_attributes": True}


class CreateIntentRequest(BaseModel):
    name: str
    description: str = ""
    keywords: list[str] = []


class UpdateIntentRequest(BaseModel):
    name: str | None = None
    description: str | None = None
    keywords: list[str] | None = None


def _to_response(space: IntentSpace, doc_count: int) -> IntentSpaceResponse:
    return IntentSpaceResponse(
        id=space.id,
        name=space.name,
        description=space.description,
        keywords=json.loads(space.keywords) if space.keywords else [],
        document_count=doc_count,
        is_default=space.is_default,
        created_at=space.created_at,
    )


@router.get("")
def list_spaces(db: Session = Depends(get_db)) -> list[IntentSpaceResponse]:
    spaces = list_intent_spaces(db)
    return [_to_response(s, get_document_count(s.id, db)) for s in spaces]


@router.post("", status_code=201)
def create_space(body: CreateIntentRequest, db: Session = Depends(get_db)) -> IntentSpaceResponse:
    try:
        space = create_intent_space(body.name, body.description, body.keywords, db)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    return _to_response(space, 0)


@router.put("/{space_id}")
def update_space(
    space_id: int, body: UpdateIntentRequest, db: Session = Depends(get_db)
) -> IntentSpaceResponse:
    try:
        space = update_intent_space(space_id, body.name, body.description, body.keywords, db)
    except ValueError as exc:
        code = 404 if "not found" in str(exc).lower() else 400
        raise HTTPException(status_code=code, detail=str(exc))
    return _to_response(space, get_document_count(space.id, db))


@router.delete("/{space_id}")
def delete_space(space_id: int, db: Session = Depends(get_db)) -> dict:
    try:
        delete_intent_space(space_id, db)
    except ValueError as exc:
        code = 404 if "not found" in str(exc).lower() else 400
        raise HTTPException(status_code=code, detail=str(exc))
    return {"message": "Intent space deleted successfully"}
