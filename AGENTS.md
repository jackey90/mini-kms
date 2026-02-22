# AGENTS.md — IntelliKnow KMS AI Development Guide

> This file is the main entry point for AI coding assistants (Cursor). All agents must read this file before starting work.

## Project Overview

**IntelliKnow KMS** — Enterprise-grade Gen AI Knowledge Management System

| Attribute | Value |
|-----------|-------|
| Project Type | Tech Lead interview project (7 days) |
| Core Requirements | `AD, Tech Lead, AKP.md` |
| Development Process | `software_rnd_full_process.md` |
| Tech Stack | Python (FastAPI + Streamlit) + SQLite/FAISS + OpenAI API |

**Core Features**:
1. Multi-frontend integration (Telegram + Microsoft Teams)
2. Document-driven knowledge base (PDF/DOCX auto-parsing)
3. Query intent orchestrator (HR/Legal/Finance classification routing)

See `AD, Tech Lead, AKP.md` for complete requirements.

---

## Agent Index

Each development phase has a corresponding agent instruction file in `.cursor/agents/`:

| Agent File | Phase | Directory | Branch Prefix |
|-----------|-------|-----------|---------------|
| `discovery-agent.md` | Market & User Research | `discovery/` | `discovery/` |
| `prd-agent.md` | Product Definition (PRD) | `prd/` | `prd/` |
| `architecture-agent.md` | Solution & Architecture | `architecture/` | `arch/` |
| `frontend-agent.md` | Frontend Development | `frontend/` | `frontend/` |
| `backend-agent.md` | Backend Development | `backend/` | `backend/` |
| `qa-agent.md` | Testing & Quality | `qa/` | `qa/` |
| `release-agent.md` | Release & Launch | `release/` | `release/` |

**Usage**: In Cursor, @ the relevant phase directory, or state which phase you're in and the agent will read the corresponding instruction file.

---

## Memory System

### Purpose
Record daily discussion content, decision conclusions, and open questions as a "decision log" for the project.

### Directory
All records stored in `memory/` directory, named by date: `memory/YYYY-MM-DD.md`

### File Format

```markdown
# YYYY-MM-DD Project Discussion Log

## Discussion Notes
(Key content from today's conversation)

## Conclusions & Decisions
(Confirmed technical/product/architecture decisions, format: ✅ Decision)

## Open Questions
(Unresolved questions, format: ❓ Question)

## Related Tasks
(STATUS.md files affected by today's discussion, format: - phase/STATUS.md)
```

### Agent Rules for Updating Memory
- After confirming a key decision with the user, write the conclusion into today's memory file under "Conclusions & Decisions"
- Ambiguous requirements encountered during conversation go into "Open Questions"
- After completing a phase, record it in the "Related Tasks" section of the memory file

---

## STATUS.md Convention

Each phase directory has a `STATUS.md` file tracking task progress.

### Task Status Markers
| Marker | Meaning |
|--------|---------|
| `[ ]` | Not started |
| `[~]` | In progress |
| `[x]` | Completed |
| `[?]` | Needs confirmation (requires user input) |
| `[!]` | Blocked (unresolved dependency) |

### Agent Rules for Updating STATUS.md
1. Before starting a subtask, mark it as `[~]`
2. When complete, change to `[x]` and add a completion timestamp with memory link
3. When something is unclear, mark `[?]` and record the question in today's memory file

---

## Git Branch & Commit Convention

### Branch Naming

```
<phase>/<short-description>
```

Examples:
- `prd/functional-requirements`
- `arch/api-contract-design`
- `frontend/admin-dashboard`
- `backend/document-parser`
- `qa/integration-test`
- `release/v1.0.0`

### Commit Message Format

**English only.** Format:

```
[phase] Short imperative description

Memory: memory/YYYY-MM-DD.md
```

Examples:
```
[prd] Add functional requirements FR-01 to FR-06

Memory: memory/2026-02-21.md
```

```
[arch] Define REST API contract and data model

Memory: memory/2026-02-22.md
```

### Rules
- Each phase's work is done on the corresponding branch, then merged to `main`
- Every commit must include the `Memory:` line pointing to the memory file with the decision context
- Changes from different phases must not be mixed in one commit

---

## Agent General Rules

1. **Read context first**: Before starting work, read `AD, Tech Lead, AKP.md`, the current phase's `STATUS.md`, and the latest `memory/` file
2. **Always confirm ambiguity**: When requirements are unclear, record the question in the memory file and ask the user — do not assume
3. **Update progress**: After completing each subtask, immediately update `STATUS.md` and the root `PROJECT_STATUS.md`
4. **Record decisions**: After every confirmed decision with the user, write it into today's memory file
5. **Atomic commits**: Each commit contains exactly one logical unit of change
6. **No cross-phase mixing**: Do not include other phase changes in the current phase's commits

## Language Convention

| File Type | Language |
|-----------|----------|
| Source code (all languages) | **English only** |
| Code comments | **English only** |
| Technical design docs (HLD/LLD/API Contract/Data Model/Algorithm Arch) | **English only** |
| README.md / AI-USAGE.md | **English only** |
| Git commit messages | **English only** |
| STATUS.md (progress tracking) | **English only** |
| memory/ (discussion logs) | **English only** |
| AGENTS.md / agent instruction files | **English only** |
