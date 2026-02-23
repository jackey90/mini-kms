import json
import time
import datetime
from dataclasses import dataclass, field
from sqlalchemy.orm import Session

from src.db.models import IntentSpace, Document, QueryLog
from src.ml.intent_classifier import classify_intent
from src.ml.embedder import embed_query
from src.ml.vector_store import vector_store
from src.ml.rag_engine import generate_response
from src.config import settings


@dataclass
class QueryResult:
    query_id: int
    answer: str
    detected_intent: str
    confidence: float
    source_documents: list[str]
    channel_formatted: str
    fallback: bool
    response_time_ms: int


def process_query(query: str, channel: str, user_id: str | None, db: Session) -> QueryResult:
    """Main orchestration pipeline: classify → retrieve → generate → log."""
    start_time = time.time()

    # 1. Load intent spaces for classification
    spaces = db.query(IntentSpace).all()
    intent_space_list = [
        {
            "name": s.name,
            "description": s.description,
            "keywords": json.loads(s.keywords),
        }
        for s in spaces
    ]

    # 2. Classify intent
    detected_intent, confidence = classify_intent(query, intent_space_list)

    # 3. Determine which FAISS index to search
    intent_space_id: int | None = None
    if detected_intent != "general":
        space = db.query(IntentSpace).filter_by(name=detected_intent).first()
        if space:
            intent_space_id = space.id

    # 4. Load recent conversation history for this user (same channel)
    conversation_history: list[dict] = []
    if user_id:
        limit = settings.conversation_history_limit
        recent_logs = (
            db.query(QueryLog)
            .filter(QueryLog.user_id == user_id, QueryLog.channel == channel)
            .order_by(QueryLog.timestamp.desc())
            .limit(limit)
            .all()
        )
        # Reverse to chronological order (oldest first) for the LLM
        for log in reversed(recent_logs):
            conversation_history.append({"role": "user", "content": log.user_query})
            if log.agent_response:
                conversation_history.append({"role": "assistant", "content": log.agent_response})

    # 5. Embed query and retrieve chunks
    query_embedding = embed_query(query)
    chunks = vector_store.search(intent_space_id, query_embedding, k=5)

    # 6. Generate RAG response
    fallback = detected_intent == "general" or not chunks
    answer, source_docs, channel_formatted = generate_response(
        query, chunks, channel, conversation_history
    )

    response_time_ms = int((time.time() - start_time) * 1000)
    response_status = "fallback" if fallback or not source_docs else "success"

    # 7. Increment access_count for source documents
    if source_docs:
        db.query(Document).filter(
            Document.filename.in_(source_docs)
        ).update(
            {Document.access_count: Document.access_count + 1},
            synchronize_session=False,
        )

    # 8. Log the query and persist the agent response
    log = QueryLog(
        user_query=query,
        agent_response=answer,
        detected_intent=detected_intent,
        confidence_score=confidence,
        source_documents=json.dumps(source_docs),
        response_status=response_status,
        channel=channel,
        user_id=user_id,
        response_time_ms=response_time_ms,
    )
    db.add(log)
    db.commit()
    db.refresh(log)

    return QueryResult(
        query_id=log.id,
        answer=answer,
        detected_intent=detected_intent,
        confidence=confidence,
        source_documents=source_docs,
        channel_formatted=channel_formatted,
        fallback=fallback or not source_docs,
        response_time_ms=response_time_ms,
    )
