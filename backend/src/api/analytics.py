import json
import datetime
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
from src.db.database import get_db
from src.services.analytics_service import get_query_logs, get_kb_stats, export_csv

router = APIRouter(prefix="/analytics", tags=["analytics"])


class QueryLogResponse(BaseModel):
    id: int
    timestamp: datetime.datetime
    user_query: str
    detected_intent: str
    confidence_score: float
    source_documents: list[str]
    response_status: str
    channel: str
    response_time_ms: int | None

    model_config = {"from_attributes": True}


class QueryLogsPage(BaseModel):
    total: int
    items: list[QueryLogResponse]


@router.get("/queries")
def query_history(
    limit: int = 50,
    offset: int = 0,
    intent: str | None = None,
    channel: str | None = None,
    date_from: str | None = None,
    date_to: str | None = None,
    db: Session = Depends(get_db),
) -> QueryLogsPage:
    limit = min(limit, 200)
    total, logs = get_query_logs(db, limit, offset, intent, channel, date_from, date_to)
    items = [
        QueryLogResponse(
            id=log.id,
            timestamp=log.timestamp,
            user_query=log.user_query,
            detected_intent=log.detected_intent,
            confidence_score=log.confidence_score,
            source_documents=json.loads(log.source_documents) if log.source_documents else [],
            response_status=log.response_status,
            channel=log.channel,
            response_time_ms=log.response_time_ms,
        )
        for log in logs
    ]
    return QueryLogsPage(total=total, items=items)


@router.get("/kb-usage")
def kb_usage(db: Session = Depends(get_db)) -> dict:
    return get_kb_stats(db)


@router.get("/export")
def export_logs(db: Session = Depends(get_db)) -> StreamingResponse:
    csv_content = export_csv(db)
    return StreamingResponse(
        iter([csv_content]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=query_logs.csv"},
    )
