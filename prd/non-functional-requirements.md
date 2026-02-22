# IntelliKnow KMS — Non-Functional Requirements

---

## NFR-01 Performance

| ID | Requirement | Metric | Priority |
|----|-------------|--------|----------|
| NFR-01-1 | Bot end-to-end response latency | ≤ 3 seconds (from user sending message to Bot reply, including intent classification + retrieval + LLM generation) | P0 |
| NFR-01-2 | Admin UI page load time | ≤ 2 seconds (initial render, local network) | P1 |
| NFR-01-3 | Document parsing time | ≤ 60 seconds (single PDF/DOCX ≤ 10MB) | P1 |
| NFR-01-4 | FAISS vector search latency | ≤ 500ms (KB with ≤ 100 documents) | P0 |

**Note**: NFR-01-1 is the most critical constraint, directly impacting user experience. LLM call (gpt-3.5-turbo) typically takes 1-2 seconds, FAISS search < 100ms — overall can satisfy the 3-second requirement.

---

## NFR-02 Concurrency & Availability

| ID | Requirement | Metric | Priority |
|----|-------------|--------|----------|
| NFR-02-1 | Concurrent query support | MVP: ≥ 5 concurrent queries without errors | P1 |
| NFR-02-2 | Service startup time | All services ready within 30 seconds after `docker-compose up` | P1 |
| NFR-02-3 | Local runtime stability | No crashes during demo session (1 hour) | P0 |

**Note**: MVP is single-machine local deployment; high availability (HA) is not required; no load balancing needed.

---

## NFR-03 Security

| ID | Requirement | Description | Priority |
|----|-------------|-------------|----------|
| NFR-03-1 | API Keys not stored in plaintext | Telegram Token / Teams App Password / OpenAI API Key all managed via environment variables (`.env`); no plaintext in code | P0 |
| NFR-03-2 | `.env` not committed to git | `.gitignore` must include `.env`; provide `.env.example` template | P0 |
| NFR-03-3 | Admin UI no authentication (MVP) | No login functionality in MVP; assumes local intranet use; README must note this limitation | P0 (risk accepted) |
| NFR-03-4 | File type validation | Upload accepts only `.pdf` and `.docx`; double validation on backend (MIME type + extension) | P0 |
| NFR-03-5 | File size limit | Single file ≤ 50MB to prevent resource exhaustion | P1 |

---

## NFR-04 Deployability

| ID | Requirement | Description | Priority |
|----|-------------|-------------|----------|
| NFR-04-1 | Docker Compose one-command startup | `docker-compose up` starts all services (FastAPI backend + Streamlit Admin UI) | P0 |
| NFR-04-2 | Zero external service dependencies | Except for OpenAI API, all storage (SQLite/FAISS) runs locally; no Redis/PostgreSQL required | P0 |
| NFR-04-3 | Data persistence | DB files and FAISS index persisted via Docker Volume; data survives container restarts | P0 |
| NFR-04-4 | Cross-platform support | Docker Compose runs on macOS / Linux / Windows (WSL2) | P1 |
| NFR-04-5 | Reproducible in clean environment | README Quick Start steps succeed in a fresh environment (only Docker + API Keys needed) | P0 |

---

## NFR-05 Observability

| ID | Requirement | Description | Priority |
|----|-------------|-------------|----------|
| NFR-05-1 | Request logging | FastAPI logs all API requests (time / path / status code / duration) to stdout | P1 |
| NFR-05-2 | Error logging | Document parsing failures and LLM call failures written to logs | P0 |
| NFR-05-3 | Health check endpoint | `GET /api/health` returns service status | P1 |
| NFR-05-4 | Document processing status tracking | Admin UI shows document processing status (Pending / Processing / Processed / Error) | P0 |

---

## NFR-06 Maintainability

| ID | Requirement | Description | Priority |
|----|-------------|-------------|----------|
| NFR-06-1 | Code language convention | All code and comments in English | P0 |
| NFR-06-2 | README completeness | Includes: project description, tech stack, local startup steps (≤ 10 steps), integration config guide | P0 |
| NFR-06-3 | `.env.example` completeness | Each environment variable has a comment explaining its purpose and how to obtain it | P0 |
| NFR-06-4 | API documentation | FastAPI auto-generates OpenAPI docs (`/docs`); no additional maintenance needed | P1 |

---

## Constraints Summary

| Constraint Type | Content |
|-----------------|---------|
| Time constraint | Complete MVP in 7 calendar days |
| Tech constraint | Lightweight stack only (SQLite/FAISS); no complex cloud services |
| Deployment constraint | Local Docker Compose; no cloud deployment |
| Budget constraint | Only OpenAI API cost (estimated < $5 during demo) |
| Team constraint | Solo development; no external collaboration |
