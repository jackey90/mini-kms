# IntelliKnow KMS — Project Status

> Single source of truth for overall project progress.
> Updated by each agent after completing tasks. For details, open the phase-specific `STATUS.md`.

## Overall Progress

| Phase | Directory | Status | Progress |
|-------|-----------|--------|----------|
| Discovery | `discovery/` | ✅ Done | 100% |
| PRD | `prd/` | ✅ Done | 100% |
| Architecture | `architecture/` | 🟡 In Setup | 10% |
| Frontend | `frontend/` | ⬜ Blocked | 0% |
| Backend | `backend/` | ⬜ Blocked | 0% |
| QA | `qa/` | ⬜ Blocked | 0% |
| Release | `release/` | ⬜ Blocked | 0% |

**Status Legend**: ⬜ Not started &nbsp;|&nbsp; 🟡 In progress &nbsp;|&nbsp; 🔴 Blocked &nbsp;|&nbsp; ✅ Done

---

## Confirmed Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js (React) + Tailwind CSS |
| Backend | Python FastAPI |
| LLM | OpenAI API — `gpt-3.5-turbo` |
| Embedding | OpenAI — `text-embedding-3-small` |
| Vector Store | FAISS (local) |
| Relational DB | SQLite |
| Document Parsing | LangChain (PDF + DOCX) |
| Integrations | Telegram Bot + Microsoft Teams Bot |
| Deployment | Docker Compose (local) |

---

## Key Decisions Log

| Date | Decision | Memory |
|------|----------|--------|
| 2026-02-21 | Frontend: Next.js (React) + Tailwind CSS | [2026-02-21](memory/2026-02-21.md) |
| 2026-02-21 | 2nd integration: Microsoft Teams | [2026-02-21](memory/2026-02-21.md) |
| 2026-02-21 | Deployment: local Docker Compose | [2026-02-21](memory/2026-02-21.md) |
| 2026-02-21 | LLM: OpenAI API (gpt-3.5-turbo) | [2026-02-21](memory/2026-02-21.md) |

---

## Open Questions

> None at this time. All initial decisions confirmed.

---

## Phase Details

### Discovery `discovery/STATUS.md` ✅
- [x] Project background & constraints confirmed
- [x] Competitive analysis (Notion AI / Guru / Confluence / Document360 / Tettra)
- [x] Tech trends (RAG, multi-channel Bot, lightweight self-hosting)
- [x] Differentiation positioning
- [x] User personas: Admin + End User
- [x] 4 core use cases + user journey maps
- [x] Problem statement, value proposition, success metrics
- [x] Assumption list (A-01 ~ A-05) with validation plan

### PRD `prd/STATUS.md` ✅
- [x] scope.md: MVP boundary (P0/P1/P2), 14 non-goals, Day 1-7 milestone plan
- [x] functional-requirements.md: FR-01~FR-06 (23 requirements with user stories)
- [x] non-functional-requirements.md: NFR-01~NFR-06 (performance/security/deployability)
- [x] acceptance-criteria.md: 30 Given/When/Then criteria in English

### Architecture `architecture/STATUS.md`
- [x] Tech stack fully confirmed
- [ ] HLD (system diagram, module boundaries)
- [ ] LLD (package structure, interfaces)
- [ ] API Contract
- [ ] Data model / SQLite schema
- [ ] Algorithm architecture (RAG pipeline)
- [ ] UI wireframes

### Frontend `frontend/STATUS.md`
- [x] Framework confirmed: Next.js (React)
- [!] Blocked: waiting for API Contract

### Backend `backend/STATUS.md`
- [x] 2nd integration confirmed: Teams
- [x] LLM confirmed: OpenAI API
- [!] Blocked: waiting for LLD + API Contract

### QA `qa/STATUS.md`
- [!] Blocked: waiting for frontend + backend completion

### Release `release/STATUS.md`
- [x] Deployment method confirmed: Docker Compose
- [!] Blocked: waiting for QA sign-off

---

*Last updated: 2026-02-21 — PRD phase complete*
