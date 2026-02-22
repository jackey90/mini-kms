# IntelliKnow KMS — Low-Level Design (LLD)

## 1. Backend Package Structure

```
backend/
├── main.py                         # FastAPI app factory, lifespan, router registration
├── requirements.txt
├── .env.example
├── src/
│   ├── api/                        # HTTP route handlers
│   │   ├── __init__.py
│   │   ├── documents.py            # /api/documents CRUD
│   │   ├── intents.py              # /api/intents CRUD
│   │   ├── query.py                # /api/query  (orchestrator entry)
│   │   ├── integrations.py         # /api/integrations config + test + Teams webhook
│   │   ├── analytics.py            # /api/analytics queries/kb-usage/export
│   │   └── health.py               # /api/health
│   ├── services/                   # Business logic (call ML + DB, no HTTP knowledge)
│   │   ├── __init__.py
│   │   ├── document_service.py     # validate, save, trigger parse pipeline
│   │   ├── intent_service.py       # CRUD for intent_spaces table
│   │   ├── orchestrator.py         # classify → retrieve → generate → log
│   │   ├── integration_service.py  # manage integration configs, test connections
│   │   └── analytics_service.py    # query logs, KB stats, CSV export
│   ├── ml/                         # AI/ML logic (pure functions, testable)
│   │   ├── __init__.py
│   │   ├── document_parser.py      # LangChain loaders + text splitting
│   │   ├── embedder.py             # OpenAI embedding calls
│   │   ├── vector_store.py         # FAISS index CRUD (load/save/add/search)
│   │   ├── intent_classifier.py    # gpt-3.5-turbo zero-shot classification
│   │   └── rag_engine.py           # context assembly + LLM response generation
│   ├── db/                         # Database layer
│   │   ├── __init__.py
│   │   ├── database.py             # SQLAlchemy engine, session factory, init_db()
│   │   └── models.py               # SQLAlchemy ORM models
│   ├── integrations/               # Bot runners (run alongside FastAPI)
│   │   ├── __init__.py
│   │   ├── telegram_bot.py         # python-telegram-bot polling handler
│   │   └── teams_bot.py            # botbuilder-python activity handler
│   └── config.py                   # Settings via pydantic-settings (.env loading)
└── tests/
    ├── test_document_service.py
    ├── test_intent_classifier.py
    └── test_orchestrator.py
```

---

## 2. Frontend Package Structure

```
frontend/
├── app.py                          # Streamlit entry — Dashboard home page
├── requirements.txt
├── pages/
│   ├── 1_KB_Management.py          # Document upload + list
│   ├── 2_Intent_Config.py          # Intent spaces + query log
│   ├── 3_Integrations.py           # Bot config + status + test
│   └── 4_Analytics.py              # Query history + KB stats + CSV export
└── utils/
    ├── api_client.py               # All HTTP calls to FastAPI backend
    └── helpers.py                  # Status badge colors, date formatting
```

---

## 3. Key Module Interfaces

### `src/config.py`

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    openai_api_key: str
    telegram_bot_token: str = ""
    teams_app_id: str = ""
    teams_app_password: str = ""
    intent_confidence_threshold: float = 0.7
    database_url: str = "sqlite:///./data/intelliknow.db"
    data_dir: str = "./data"
    max_file_size_bytes: int = 50 * 1024 * 1024  # 50MB

    class Config:
        env_file = ".env"

settings = Settings()
```

---

### `src/db/models.py`

```python
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy import Integer, String, Float, Boolean, DateTime
import datetime

class Base(DeclarativeBase):
    pass

class IntentSpace(Base):
    __tablename__ = "intent_spaces"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String, default="")
    keywords: Mapped[str] = mapped_column(String, default="[]")  # JSON
    is_default: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)

class Document(Base):
    __tablename__ = "documents"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    filename: Mapped[str] = mapped_column(String, nullable=False)
    format: Mapped[str] = mapped_column(String, nullable=False)
    size_bytes: Mapped[int] = mapped_column(Integer, nullable=False)
    file_path: Mapped[str] = mapped_column(String, nullable=False)
    intent_space_id: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String, default="pending")
    chunk_count: Mapped[int] = mapped_column(Integer, default=0)
    access_count: Mapped[int] = mapped_column(Integer, default=0)
    error_message: Mapped[str | None] = mapped_column(String, nullable=True)
    uploaded_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)
    processed_at: Mapped[datetime.datetime | None] = mapped_column(DateTime, nullable=True)

class QueryLog(Base):
    __tablename__ = "query_logs"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    timestamp: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)
    user_query: Mapped[str] = mapped_column(String, nullable=False)
    detected_intent: Mapped[str] = mapped_column(String, nullable=False)
    confidence_score: Mapped[float] = mapped_column(Float, nullable=False)
    source_documents: Mapped[str] = mapped_column(String, default="[]")  # JSON
    response_status: Mapped[str] = mapped_column(String, nullable=False)
    channel: Mapped[str] = mapped_column(String, nullable=False)
    user_id: Mapped[str | None] = mapped_column(String, nullable=True)
    response_time_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)

class Integration(Base):
    __tablename__ = "integrations"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    channel: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    token_last4: Mapped[str | None] = mapped_column(String, nullable=True)
    status: Mapped[str] = mapped_column(String, default="disconnected")
    last_active_at: Mapped[datetime.datetime | None] = mapped_column(DateTime, nullable=True)
    error_message: Mapped[str | None] = mapped_column(String, nullable=True)
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)
```

---

### `src/ml/vector_store.py` — Key Interface

```python
class VectorStore:
    def add_document(self, intent_space_id: int, chunks: list[str],
                     embeddings: list[list[float]], document_id: int,
                     filename: str) -> int: ...
    # Returns number of chunks added

    def search(self, intent_space_id: int | None,
               query_embedding: list[float], k: int = 5) -> list[dict]: ...
    # Returns: [{"chunk_text": str, "document_id": int,
    #            "filename": str, "distance": float}]
    # intent_space_id=None → search all spaces (general fallback)
```

---

### `src/services/orchestrator.py` — Key Interface

```python
async def process_query(
    query: str,
    channel: str,
    user_id: str | None,
    db: Session
) -> QueryResult:
    # 1. classify_intent()
    # 2. embed_query()
    # 3. vector_store.search()
    # 4. rag_engine.generate()
    # 5. log to query_logs
    # 6. increment document access_count
    # Returns QueryResult(answer, intent, confidence, sources, fallback)
```

---

## 4. Exception Handling Strategy

| Exception | Where caught | Response |
|-----------|-------------|----------|
| File type not PDF/DOCX | `document_service.py` | `400 Bad Request` |
| File size > 50MB | `document_service.py` | `400 Bad Request` |
| LangChain parse error (e.g. encrypted PDF) | `document_service.py` | document.status = "error", logged |
| OpenAI API timeout | `embedder.py`, `rag_engine.py` | retry once, then `500` + logged |
| OpenAI API auth error | same | `500` + logged (check .env) |
| FAISS index not found | `vector_store.py` | create new empty index |
| Intent space not found | `intent_service.py` | `404 Not Found` |
| SQLAlchemy error | all services | rollback + `500` + logged |
| Telegram API error | `telegram_bot.py` | log + update integration status |
