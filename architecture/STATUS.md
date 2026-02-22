# Architecture Phase Status

> Corresponds to development process: Phase 3 — Solution & Architecture Design

**Phase Goal**: Confirm tech stack, system boundaries, API Contract, and data model to provide a clear blueprint for development.

**Prerequisites**: All FR/NFR in `prd/STATUS.md` completed and open questions resolved.

---

## 3.1 High-Level Design (HLD)

- [x] Tech stack confirmation
  - [x] Frontend framework: **Streamlit (Python)** (Option A recommended stack; faster to build for MVP within 7 days)
  - [x] Backend: FastAPI (Python)
  - [x] Document parsing: LangChain Document Loaders (PyPDFLoader + Docx2txtLoader)
  - [x] Vector store: FAISS (local persistence)
  - [x] Relational store: SQLite
  - [x] LLM: **OpenAI API** (gpt-3.5-turbo for intent classification + response generation, text-embedding-3-small for vectorization)
- [x] System boundaries & module breakdown
- [x] Critical path design (end-to-end query processing flow)
- [x] Risk & rollback strategy
- Output: `architecture/HLD.md` ✅

## 3.2 Low-Level Design (LLD)

- [x] Module breakdown (package structure under `backend/`)
- [x] REST API Contract definition
  - [x] Document management API (upload/list/delete/reparse)
  - [x] Intent space management API (CRUD)
  - [x] Query API (submit query → return classification + response)
  - [x] Analytics API (query history, KB usage stats)
  - [x] Frontend integration management API (config / connection test)
- [x] Data model / ERD (SQLite Schema)
- [x] Exception handling & degradation strategy
- Output: `architecture/LLD.md` ✅, `architecture/api-contract.md` ✅, `architecture/data-model.md` ✅

## 3.3 UX/UI Design

- [x] Information architecture (page hierarchy, navigation structure)
- [x] Key page interaction specs (text descriptions / wireframes)
  - [x] Admin Dashboard
  - [x] KB Management
  - [x] Intent Configuration
  - [x] Frontend Integration
  - [x] Analytics
- Output: `architecture/ui-wireframes.md` ✅

## 3.4 Algorithm Architecture

- [x] Document parsing pipeline (PDF/DOCX → Chunks → Embeddings → FAISS)
- [x] Vector retrieval strategy (similarity threshold, Top-K)
- [x] Intent classification approach (prompt design + confidence calculation)
- [x] RAG response generation pipeline
- Output: `architecture/algorithm-arch.md` ✅

---

## Blockers / Open Questions

> ✅ **[Confirmed]** Frontend framework: **Streamlit (Python)** — Option A recommended stack (2026-02-21, revised)
> See: [memory/2026-02-21.md](../memory/2026-02-21.md)

> ✅ **[Confirmed]** Deployment: **Local Docker Compose Demo** (2026-02-21)
> See: [memory/2026-02-21.md](../memory/2026-02-21.md)

> ✅ **[Confirmed]** LLM: **OpenAI API** (gpt-3.5-turbo + text-embedding-3-small) (2026-02-21)
> See: [memory/2026-02-21.md](../memory/2026-02-21.md)

---

## Completion Log

| Time | Completed | Memory Link |
|------|-----------|-------------|
| 2026-02-21 | Architecture phase scaffolding | [memory/2026-02-21.md](../memory/2026-02-21.md) |
