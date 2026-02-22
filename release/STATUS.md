# Release Phase Status

> Corresponds to development process: Phase 7 — Release & Launch + Section 3.3 Delivery Requirements

**Phase Goal**: Complete GitHub repo publication, Demo deployment, and README documentation to meet interview delivery requirements.

**Prerequisites**: All UAT tests in `qa/STATUS.md` must pass.

---

## 7.1 Release Preparation

- [ ] Version number confirmed (v1.0.0 MVP)
- [ ] Code cleanup (remove debug code, redact sensitive comments)
- [ ] Dependency version pinning (`requirements.txt` with fixed versions)
- [ ] Environment variables documented (`.env.example` complete)
- [ ] Rollback plan (local demo: roll back to previous git tag)

## 7.2 GitHub Repository Preparation

- [ ] Repository set to Public
- [ ] README.md completeness check
  - [ ] Project description (What & Why)
  - [ ] Tech stack overview
  - [ ] Local startup steps (step-by-step)
  - [ ] Frontend integration config guide (Telegram / Teams setup steps)
  - [ ] API docs index (link to `architecture/api-contract.md`)
  - [ ] AI usage reflection (`AI-USAGE.md` or README section)
- [ ] Sample data preparation (2 sample documents: 1 PDF + 1 DOCX)
- [ ] `.gitignore` verification (`.env`, `*.db`, `faiss_index/` excluded)

## 7.3 Demo Deployment

- [x] Deployment method confirmed: **Local Demo + Docker Compose**
- [ ] `docker-compose.yml` (one-command startup for FastAPI + Next.js + data volumes)
- [ ] Local startup documentation (Quick Start in README)

## 7.4 AI Usage Reflection Document (explicitly required)

- [ ] `AI-USAGE.md` created
  - [ ] Scenario 1: AI usage in document parsing (PDF table extraction case)
  - [ ] Scenario 2: AI usage in frontend integration (response format adaptation case)
  - [ ] Strategic intent of AI usage (not tool names)
  - [ ] Adjustments made to AI outputs

## 7.5 Go-Live Validation

- [ ] Full demo flow walkthrough (upload document → Telegram query → receive answer)
- [ ] Known issues list documented
- [ ] Go/No-Go decision

---

## Blockers / Open Questions

> ✅ **[Confirmed]** Deployment: Local Demo + Docker Compose (2026-02-21)
> See: [memory/2026-02-21.md](../memory/2026-02-21.md)

---

## Completion Log

| Time | Completed | Memory Link |
|------|-----------|-------------|
| 2026-02-21 | Release phase scaffolding | [memory/2026-02-21.md](../memory/2026-02-21.md) |
