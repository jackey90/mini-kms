# IntelliKnow KMS — High-Level Design (HLD)

## 1. Tech Stack

| Layer | Technology | Rationale |
|-------|-----------|-----------|
| Admin UI | Streamlit (Python 3.11) | Option A recommended stack; same language as backend; fastest Admin UI for MVP |
| Backend API | FastAPI (Python 3.11) | Async, auto-generates OpenAPI docs, production-grade |
| Intent Classification | OpenAI `gpt-3.5-turbo` | Zero-shot classification, no training data needed |
| Embeddings | OpenAI `text-embedding-3-small` | Cost-efficient, 1536-dim, compatible with FAISS |
| Vector Store | FAISS (local, persisted) | Lightweight, no server required, fast ANN search |
| Relational DB | SQLite (via SQLAlchemy) | Zero-config, file-based, sufficient for MVP single-machine |
| Document Parsing | LangChain (PyPDFLoader + Docx2txtLoader) | Handles PDF/DOCX with tables |
| Bot Integration 1 | Telegram Bot API (polling) | No public URL needed for local demo |
| Bot Integration 2 | Microsoft Teams (Bot Framework SDK) | Bot Framework Emulator for local testing |
| Deployment | Docker Compose | One-command startup, no cloud dependency |

---

## 2. System Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                     USER CHANNELS                                 │
│  ┌─────────────────┐        ┌──────────────────────────────┐     │
│  │  Telegram Client │        │  Microsoft Teams Client      │     │
│  └────────┬─────────┘        └──────────────┬───────────────┘     │
└───────────┼──────────────────────────────────┼────────────────────┘
            │ Bot API (polling)                 │ Bot Framework SDK
            ▼                                   ▼
┌──────────────────────────────────────────────────────────────────┐
│                     BACKEND (FastAPI :8000)                       │
│                                                                    │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────────────────┐   │
│  │  /documents  │  │  /intents    │  │  /query               │   │
│  │  (CRUD)      │  │  (CRUD)      │  │  (orchestrator entry) │   │
│  └──────────────┘  └──────────────┘  └──────────┬────────────┘   │
│                                                   │               │
│  ┌────────────────────────────────────────────────▼────────────┐  │
│  │               QUERY ORCHESTRATOR                            │  │
│  │   1. Intent Classifier (gpt-3.5-turbo zero-shot)           │  │
│  │   2. FAISS Retrieval (top-5 chunks per intent space)       │  │
│  │   3. RAG Response Generator (gpt-3.5-turbo + citations)    │  │
│  └─────────────────────────────────────────────────────────────┘  │
│                                                                    │
│  ┌──────────────┐  ┌──────────────────┐  ┌───────────────────┐   │
│  │  /integ.     │  │  /analytics      │  │  /health          │   │
│  │  (Tg/Teams)  │  │  (logs/export)   │  │  (health check)   │   │
│  └──────────────┘  └──────────────────┘  └───────────────────┘   │
└─────────────────────────────┬────────────────────────────────────┘
                              │
            ┌─────────────────┼─────────────────┐
            ▼                 ▼                  ▼
   ┌─────────────┐   ┌──────────────┐   ┌──────────────────┐
   │   SQLite    │   │    FAISS     │   │   File Storage   │
   │  metadata   │   │  (per-intent │   │  /data/uploads/  │
   │  query_logs │   │   indexes)   │   │                  │
   └─────────────┘   └──────────────┘   └──────────────────┘
            │
            ▼
   ┌─────────────────────────────────┐
   │   OpenAI API                    │
   │   - text-embedding-3-small      │
   │   - gpt-3.5-turbo               │
   └─────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│              ADMIN UI (Streamlit :8501)                           │
│  app.py           → Dashboard (metrics overview)                  │
│  1_KB_Management  → Upload / list / delete documents              │
│  2_Intent_Config  → Manage intent spaces + query log              │
│  3_Integrations   → Configure and test Bot connections            │
│  4_Analytics      → Query history + KB usage + CSV export         │
└──────────────────────────────────────────────────────────────────┘
         │ HTTP (requests lib → localhost:8000)
         └──────────────────────────────────────▶ FastAPI Backend
```

---

## 3. Module Boundaries

| Module | Location | Responsibility |
|--------|----------|----------------|
| API Router | `backend/src/api/` | HTTP endpoints, request validation, response serialization |
| Services | `backend/src/services/` | Business logic; calls ML modules and DB |
| ML Pipeline | `backend/src/ml/` | Document parsing, embedding, FAISS, intent classification, RAG |
| Database | `backend/src/db/` | SQLAlchemy models, session management, migrations |
| Integrations | `backend/src/integrations/` | Telegram/Teams bot polling and message dispatch |
| Admin UI | `frontend/` | Streamlit pages, each page calls API via `utils/api_client.py` |

---

## 4. Critical Query Path (P0)

```
User sends message (Telegram / Teams)
        │
        ▼
[Integration Module] receives message
        │ POST /api/query
        ▼
[Query Orchestrator]
   ├── 1. Classify intent (gpt-3.5-turbo, ~0.5s)
   │       └── confidence ≥ 0.7 → use intent space
   │           confidence < 0.7 → use "general" (all docs)
   ├── 2. Embed query (text-embedding-3-small, ~0.2s)
   ├── 3. FAISS search top-5 (< 50ms)
   ├── 4. Assemble context + generate response (gpt-3.5-turbo, ~1.5s)
   └── 5. Log to SQLite + return response
        │
        ▼
[Integration Module] formats + sends reply to user
Total target: ≤ 3 seconds
```

---

## 5. Data Flow: Document Ingestion

```
Admin uploads PDF/DOCX via Streamlit
        │ POST /api/documents (multipart)
        ▼
[Document Service]
   ├── 1. Validate (type: pdf/docx, size: ≤50MB)
   ├── 2. Save file to /data/uploads/{id}_{filename}
   ├── 3. Update SQLite status → "processing"
   ├── 4. LangChain loader → extract text chunks
   ├── 5. OpenAI embed each chunk
   ├── 6. Add vectors to FAISS index (intent-space-partitioned)
   ├── 7. Persist FAISS index to /data/faiss/{intent_space_id}.index
   └── 8. Update SQLite status → "processed", store chunk count
```

---

## 6. FAISS Index Strategy

Each intent space has its own FAISS index file:
- `data/faiss/intent_{id}.index` — the FAISS IndexFlatL2 index
- `data/faiss/intent_{id}_meta.json` — chunk-to-document mapping (for citations)

When "General" fallback is needed, all intent space indexes are searched and results merged.

---

## 7. Risk Register

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| OpenAI API latency spikes | Medium | Bot response > 3s | gpt-3.5-turbo is fast; add timeout + retry |
| Teams Bot Azure registration complexity | High | Day 4 blocker | Mock Teams endpoint if registration takes > 4h |
| FAISS index corruption on crash | Low | Data loss | Auto-persist after every document addition |
| Streamlit session state loss on reload | Low | UX degradation | Use st.session_state for all filter/form values |
