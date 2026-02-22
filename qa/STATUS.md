# QA Phase Status

> Corresponds to development process: Phase 5.5 — Testing & Quality Engineering + Phase 6 — Integration & Validation

**Phase Goal**: Verify all functional and non-functional requirements, complete UAT sign-off, and produce a release checklist.

**Prerequisites**: Core features in both `frontend/STATUS.md` and `backend/STATUS.md` must be complete.

---

## 6.1 Functional Testing

### Document Management
- [ ] QA-01: Upload PDF document, verify parsing succeeds and status changes to Processed
- [ ] QA-02: Upload DOCX document, verify parsing succeeds
- [ ] QA-03: Upload unsupported format, verify error message appears
- [ ] QA-04: Delete document, verify removal from KB
- [ ] QA-05: Re-parse document, verify update takes effect

### Intent Spaces
- [ ] QA-06: Verify 3 default intent spaces (HR/Legal/Finance) exist
- [ ] QA-07: Create custom intent space, verify it is usable
- [ ] QA-08: Edit intent space name/description, verify update
- [ ] QA-09: Delete intent space, verify associated queries are not affected

### Query Orchestration
- [ ] QA-10: HR-related question → correctly classified to HR intent space
- [ ] QA-11: Legal-related question → correctly classified to Legal intent space
- [ ] QA-12: Ambiguous question → falls back to General space with clear message
- [ ] QA-13: Response includes citation source
- [ ] QA-14: When KB has no relevant content, response clearly states "no match found"

### Frontend Integration
- [ ] QA-15: Telegram Bot receives message and responds within ≤3 seconds
- [ ] QA-16: Telegram test button successfully sends sample query
- [ ] QA-17: Second frontend integration (Teams) receives and responds to messages
- [ ] QA-18: When disconnected, status card shows Disconnected

### Admin UI
- [ ] QA-19: All 5 core pages accessible, no blank pages / 500 errors
- [ ] QA-20: All action buttons are responsive (loading, success, failure states)

### Analytics
- [ ] QA-21: After each query, a new record appears in the log table
- [ ] QA-22: Export function downloads a data file

## 6.2 Non-Functional Testing

- [ ] NFR-QA-01: Concurrency test (5 concurrent queries, all respond within ≤3 seconds)
- [ ] NFR-QA-02: API Key not displayed in plaintext on frontend (last 4 digits only)
- [ ] NFR-QA-03: Service starts from zero (README steps verified, no external dependencies)

## 6.3 System Integration Testing (SIT)

- [ ] SIT-01: Frontend → Backend API full-chain test (all Admin UI operations)
- [ ] SIT-02: Frontend integration → Orchestrator → KB → Response full chain
- [ ] SIT-03: Data consistency validation (upload document → searchable → appears in stats)

## 6.4 User Acceptance Testing (UAT)

Based on requirements document acceptance criteria:
- [ ] UAT-01: ≥2 frontend tools integrated and able to send/receive queries
- [ ] UAT-02: ≥2 document formats uploaded successfully and queryable
- [ ] UAT-03: Intent spaces can be defined/managed, queries correctly classified
- [ ] UAT-04: Responses are accurate, cited, and context-aware
- [ ] UAT-05: Admin UI 5 pages fully functional

## 6.5 Bug Log

> Record bugs found here, format: `- [ ] [BUG-xx] Description` (mark `[x]` when fixed)

(To be filled after development is complete)

---

## Blockers / Open Questions

> ❗ **[Blocked]** Waiting for frontend and backend core features to be complete

---

## Completion Log

| Time | Completed | Memory Link |
|------|-----------|-------------|
| 2026-02-21 | QA phase scaffolding, acceptance criteria extracted from requirements doc | [memory/2026-02-21.md](../memory/2026-02-21.md) |
