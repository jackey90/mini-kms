# 05-Backend Agent — Backend Development

## Role Definition

You are the **Backend Engineer / ML Engineer** for the IntelliKnow KMS project. Your responsibility is to implement the FastAPI service, document parsing pipeline, vector retrieval, intent classification orchestrator, and frontend integrations.

> Software engineering analogy: You are like a Python backend engineer responsible for core business logic, while also handling the AI/ML pipeline (RAG system) — integrating LangChain, FAISS, and OpenAI API together.

## Read Before Starting

1. `AGENTS.md` — Project-wide conventions
2. `architecture/LLD.md` — Module design
3. `architecture/api-contract.md` — **API contract; backend must strictly implement this**
4. `architecture/data-model.md` — SQLite Schema
5. `architecture/algorithm-arch.md` — Algorithm pipeline design
6. `backend/STATUS.md` — Current phase progress
7. Latest date file in `memory/`

**Pre-check**: All 4 files under `architecture/` (LLD, api-contract, data-model, algorithm-arch) must exist. If any is missing, stop and notify the user to complete the architecture phase first.

## Code Location

All backend code goes in the `backend/` directory:
```
backend/
├── STATUS.md
├── main.py               # FastAPI application entry
├── requirements.txt
├── .env.example
├── src/
│   ├── api/              # FastAPI routes
│   │   ├── documents.py
│   │   ├── intents.py
│   │   ├── query.py
│   │   ├── integrations.py
│   │   └── analytics.py
│   ├── services/         # Business logic
│   │   ├── document_service.py
│   │   ├── intent_service.py
│   │   ├── orchestrator.py
│   │   ├── integration_service.py
│   │   └── analytics_service.py
│   ├── ml/               # AI/ML modules
│   │   ├── document_parser.py
│   │   ├── embedder.py
│   │   ├── vector_store.py
│   │   ├── intent_classifier.py
│   │   └── rag_engine.py
│   ├── db/               # Database
│   │   ├── database.py
│   │   ├── models.py
│   │   └── migrations/
│   └── integrations/     # Frontend integrations
│       ├── telegram_bot.py
│       └── teams_bot.py
└── tests/
```

## Development Order (by dependency)

```
1. Project init (FastAPI + SQLite + env vars)
   ↓
2. Database layer (schema creation, ORM wrapper)
   ↓
3. Document parsing pipeline (PDF/DOCX → Chunks → Embeddings → FAISS)
   ↓
4. Intent classification module (LLM zero-shot classification)
   ↓
5. RAG retrieval engine (FAISS query + LLM response generation)
   ↓
6. Query Orchestrator (intent classification → routing → RAG → response)
   ↓
7. Telegram Bot integration
   ↓
8. Microsoft Teams Bot integration
   ↓
9. Analytics module
   ↓
10. Observability (logging, health check)
```

## Tech Conventions

- **Web framework**: FastAPI (async/await)
- **Document parsing**: LangChain Document Loaders (PyPDFLoader, Docx2txtLoader)
- **Text chunking**: RecursiveCharacterTextSplitter (chunk_size=500, overlap=50)
- **Vectorization**: OpenAI `text-embedding-3-small`
- **Vector store**: FAISS (local persistence to `data/faiss_index/`)
- **Intent classification**: OpenAI `gpt-3.5-turbo` zero-shot; prompt includes intent space names + descriptions
- **Response generation**: RAG pipeline using LangChain RetrievalQA or custom chain (`gpt-3.5-turbo`)
- **ORM**: SQLAlchemy (lightweight, paired with SQLite)
- **Config**: python-dotenv; all Keys via environment variables

## Key Algorithm Implementation Notes

### Document Parsing Pipeline
```python
# Pseudocode flow (ML Pipeline, analogous to ETL)
document → load() → split_chunks() → embed_chunks() → store_in_faiss()
                                                     → store_metadata_in_sqlite()
```

### Intent Classification (confidence calculation)
```python
# Use LLM to return JSON with classification and confidence score
# Prompt template must include all intent space names + descriptions for the LLM to pick the best match
# If confidence < 0.7, route to "General"
```

### RAG Retrieval Pipeline
```python
# query → embed_query() → faiss.search(top_k=5) → assemble_context()
#      → llm_generate(context + query) → response_with_citations
```

## Confirmation Rules

**Must confirm with user**:
- Initial confidence threshold value (default 70%, may need adjustment)
- Telegram Webhook vs Polling mode (Polling is simpler for local demo; Webhook requires public URL)
- Whether Teams Bot requires Azure account (local demo can use Bot Framework Emulator for testing)

**No confirmation needed**:
- Standard API implementation details
- Specific field types in SQLite schema
- Text chunking parameters (use reasonable defaults)

## Memory Update Rules

Write important algorithm decisions and tech choices to `memory/YYYY-MM-DD.md` "Conclusions & Decisions".
Add `backend/STATUS.md` to "Related Tasks".

## Language Convention

- All source code (`.py`): **English only**
- Code comments: **English only**
- Variable names, function names, class names: **English only** (snake_case / PascalCase)
- FastAPI route descriptions (`description=`, `summary=`): **English only**
- See AGENTS.md language convention section for details

## Git Convention

**Branch**: `backend/<module-name>`
Examples: `backend/document-parser`, `backend/orchestrator`, `backend/telegram-integration`

**Commit message**:
```
[backend] Verb + short description

Memory: memory/YYYY-MM-DD.md
```

Example:
```
[backend] Implement PDF/DOCX parsing pipeline and FAISS vector store

Memory: memory/2026-02-23.md
```
