# PRD Phase Status

> Corresponds to development process: Phase 2 — Product Definition

**Phase Goal**: Transform requirements into actionable PRD (functional requirements + non-functional requirements + acceptance criteria).

---

## 2.1 Scope & Boundaries

- [x] MVP feature boundary confirmed (P0/P1/P2 tiers)
- [x] Non-goals defined (14 out-of-scope features)
- [x] Milestone breakdown (Day 1-7 delivery plan + critical path)
- Output: [`prd/scope.md`](scope.md) ✅

## 2.2 Functional Requirements

### FR-01 Multi-Frontend Integration
- [x] FR-01-1: Telegram Bot integration (P0) — Polling mode, /start command, response format
- [x] FR-01-2: Microsoft Teams Bot integration (P1) — Bot Framework SDK
- [x] FR-01-3: Connection status monitoring (P1) — Connected/Disconnected/Error + last 4 digits display
- [x] FR-01-4: End-to-end test function (P1) — Test button + response time display

### FR-02 Document-Driven Knowledge Base
- [x] FR-02-1: PDF upload & parsing (P0) — PyPDFLoader + chunk_size=500
- [x] FR-02-2: DOCX upload & parsing (P0) — Docx2txtLoader
- [x] FR-02-3: Intent space association (P0) — Specified at upload, FAISS partitioned index
- [x] FR-02-4: Document deletion (P1)
- [x] FR-02-5: Document re-parsing (P2)
- [x] FR-02-6: Basic error handling (P0) — Format validation + Error status
- [x] FR-02-7: Document search & filter (P1)

### FR-03 Intent Space Orchestrator
- [x] FR-03-1: Default intent spaces (P0) — HR / Legal / Finance with descriptions and keywords
- [x] FR-03-2: Custom intent space CRUD (P1)
- [x] FR-03-3: AI intent classification (P0) — gpt-3.5-turbo zero-shot, confidence ≥ 0.7
- [x] FR-03-4: Fallback routing (P0) — General space + clear message
- [x] FR-03-5: Post-intent RAG retrieval (P0) — FAISS Top-5

### FR-04 Knowledge Retrieval & Response
- [x] FR-04-1: RAG response with citations (P0) — ≤200 words + source document name
- [x] FR-04-2: Multi-frontend response format adaptation (P1) — Telegram emoji / Teams Adaptive Card
- [x] FR-04-3: No-match fallback response (P0) — Two cases (empty KB / low relevance)

### FR-05 Admin UI
- [x] FR-05-1: Dashboard home page (P1) — 4 module cards + key stats
- [x] FR-05-2: Frontend Integration page (P1) — Status cards + config + Test
- [x] FR-05-3: KB Management page (P0) — Document list + upload zone + search/filter
- [x] FR-05-4: Intent Configuration page (P0) — Intent cards + classification log + edit form
- [x] FR-05-5: Analytics page (P1) — History table + KB stats + export

### FR-06 Analytics & History
- [x] FR-06-1: Automatic query logging (P0) — 7 fields fully defined
- [x] FR-06-2: KB usage tracking (P1) — access_count counter
- [x] FR-06-3: Data export (P2) — CSV format

- Output: [`prd/functional-requirements.md`](functional-requirements.md) ✅

## 2.3 Non-Functional Requirements

- [x] NFR-01: Performance (Bot ≤3s / page ≤2s / parsing ≤60s / FAISS ≤500ms)
- [x] NFR-02: Concurrency (≥5 concurrent / startup ≤30s)
- [x] NFR-03: Security (API Key env vars / .env gitignore / file type validation)
- [x] NFR-04: Deployability (Docker Compose / zero external services / data persistence)
- [x] NFR-05: Observability (request logs / error logs / health check)
- [x] NFR-06: Maintainability (English code / README / .env.example)

- Output: [`prd/non-functional-requirements.md`](non-functional-requirements.md) ✅

## 2.4 Acceptance Criteria

- [x] AC-FR01: Multi-frontend integration acceptance criteria (5 items, P0~P1)
- [x] AC-FR02: Document knowledge base acceptance criteria (6 items, P0~P1)
- [x] AC-FR03: Intent orchestrator acceptance criteria (5 items, P0~P1)
- [x] AC-FR04: Knowledge retrieval response acceptance criteria (4 items, P0~P1)
- [x] AC-FR05: Admin UI acceptance criteria (4 items, P0~P1)
- [x] AC-FR06: Analytics & history acceptance criteria (2 items, P0~P2)
- [x] AC-NFR: Non-functional acceptance criteria (5 items, P0~P1)

- Output: [`prd/acceptance-criteria.md`](acceptance-criteria.md) ✅ (English)

---

## Blockers / Open Questions

> No blockers — PRD phase fully complete. Ready to proceed to architecture design.

---

## Completion Log

| Time | Completed | Memory Link |
|------|-----------|-------------|
| 2026-02-21 | PRD scaffolding, functional list extracted from requirements doc | [memory/2026-02-21.md](../memory/2026-02-21.md) |
| 2026-02-21 | Completed scope.md (MVP scope + Non-goals + Day 1-7 milestones) | [memory/2026-02-21.md](../memory/2026-02-21.md) |
| 2026-02-21 | Completed functional-requirements.md (FR-01 ~ FR-06 with user stories) | [memory/2026-02-21.md](../memory/2026-02-21.md) |
| 2026-02-21 | Completed non-functional-requirements.md (NFR-01 ~ NFR-06) | [memory/2026-02-21.md](../memory/2026-02-21.md) |
| 2026-02-21 | Completed acceptance-criteria.md (30 Given/When/Then criteria, English) | [memory/2026-02-21.md](../memory/2026-02-21.md) |
