from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from src.db.database import get_db
from src.services.orchestrator import process_query

router = APIRouter(prefix="/query", tags=["query"])


class QueryRequest(BaseModel):
    query: str
    channel: str = "api"
    user_id: str | None = None


class QueryResponse(BaseModel):
    query_id: int
    answer: str
    detected_intent: str
    confidence: float
    source_documents: list[str]
    channel_formatted: str
    fallback: bool
    response_time_ms: int


@router.post("")
def submit_query(body: QueryRequest, db: Session = Depends(get_db)) -> QueryResponse:
    if not body.query.strip():
        raise HTTPException(status_code=422, detail="Query cannot be empty")

    result = process_query(body.query, body.channel, body.user_id, db)

    return QueryResponse(
        query_id=result.query_id,
        answer=result.answer,
        detected_intent=result.detected_intent,
        confidence=result.confidence,
        source_documents=result.source_documents,
        channel_formatted=result.channel_formatted,
        fallback=result.fallback,
        response_time_ms=result.response_time_ms,
    )
