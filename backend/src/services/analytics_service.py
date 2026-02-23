import csv
import io
import json
from sqlalchemy.orm import Session
from sqlalchemy import func
from src.db.models import QueryLog, Document, IntentSpace

def reclassify_query(query_id: int, correct_intent: str, db: Session) -> None:
    """Admin overrides the detected intent for a query — used as a feedback signal."""
    log = db.query(QueryLog).filter_by(id=query_id).first()
    if not log:
        raise ValueError(f"Query log {query_id} not found")

    space = db.query(IntentSpace).filter_by(name=correct_intent).first()
    if not space:
        raise ValueError(f"Intent space '{correct_intent}' not found")

    log.detected_intent = correct_intent
    log.response_status = "reclassified"
    db.commit()


def get_query_logs(
    db: Session,
    limit: int = 50,
    offset: int = 0,
    intent: str | None = None,
    channel: str | None = None,
    date_from: str | None = None,
    date_to: str | None = None,
) -> tuple[int, list[QueryLog]]:
    q = db.query(QueryLog)
    if intent:
        q = q.filter(QueryLog.detected_intent == intent)
    if channel:
        q = q.filter(QueryLog.channel == channel)
    if date_from:
        q = q.filter(QueryLog.timestamp >= date_from)
    if date_to:
        q = q.filter(QueryLog.timestamp <= date_to + "T23:59:59")
    total = q.count()
    items = q.order_by(QueryLog.timestamp.desc()).offset(offset).limit(limit).all()
    return total, items


def get_kb_stats(db: Session) -> dict:
    total_docs = db.query(Document).filter(Document.status == "processed").count()
    total_queries = db.query(QueryLog).count()

    avg_latency_row = db.query(func.avg(QueryLog.response_time_ms)).scalar()
    avg_latency_ms = round(avg_latency_row) if avg_latency_row else 0

    intent_rows = (
        db.query(QueryLog.detected_intent, func.count(QueryLog.id).label("count"))
        .group_by(QueryLog.detected_intent)
        .all()
    )
    intent_distribution = [{"intent": r.detected_intent, "count": r.count} for r in intent_rows]

    top_docs = (
        db.query(Document)
        .filter(Document.status == "processed")
        .order_by(Document.access_count.desc())
        .limit(10)
        .all()
    )

    return {
        "total_documents": total_docs,
        "total_queries": total_queries,
        "avg_latency_ms": avg_latency_ms,
        "intent_distribution": intent_distribution,
        "top_documents": [
            {"filename": d.filename, "access_count": d.access_count} for d in top_docs
        ],
    }


def export_csv(db: Session) -> str:
    logs = db.query(QueryLog).order_by(QueryLog.timestamp.desc()).all()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "id", "timestamp", "user_query", "detected_intent", "confidence_score",
        "source_documents", "response_status", "channel", "response_time_ms",
    ])
    for log in logs:
        writer.writerow([
            log.id, log.timestamp, log.user_query, log.detected_intent,
            log.confidence_score, log.source_documents, log.response_status,
            log.channel, log.response_time_ms,
        ])
    return output.getvalue()
