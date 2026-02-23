# IntelliKnow KMS

> A Gen AI-powered Knowledge Management System with multi-channel Bot integration, document-driven knowledge base, and intelligent query routing.

---

## What & Why

Enterprises struggle with fragmented knowledge scattered across documents, siloed channels, and slow manual retrieval. **IntelliKnow KMS** solves this by:

1. **Meeting users where they are** — query the knowledge base directly from Telegram or Microsoft Teams, no extra login required
2. **Automating knowledge ingestion** — upload PDF/DOCX files and they are automatically parsed, chunked, and indexed for semantic search
3. **Routing intelligently** — an AI orchestrator classifies each query into the right knowledge domain (HR, Legal, Finance, or custom) before retrieving answers

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Admin UI | Streamlit (Python) |
| Backend API | FastAPI (Python 3.11) |
| LLM | OpenAI (configurable, default `gpt-3.5-turbo`) |
| Embeddings | OpenAI (configurable, default `text-embedding-3-small`) |
| Vector Store | FAISS (local, persisted) |
| Relational DB | SQLite |
| Document Parsing | LangChain (PyPDFLoader + Docx2txtLoader) |
| Bot Integration 1 | Telegram Bot API (polling) |
| Bot Integration 2 | Microsoft Teams (Bot Framework SDK) |
| Deployment | Docker Compose |

---

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) + [Docker Compose](https://docs.docker.com/compose/install/) (v2+)
- An [OpenAI API Key](https://platform.openai.com/api-keys)
- (Optional) A Telegram Bot Token from [@BotFather](https://t.me/botfather)
- (Optional) Microsoft Teams App credentials from Azure Bot registration

---

## Quick Start

### Step 1 — Clone the repository

```bash
git clone <your-repo-url>
cd mini-kms
```

### Step 2 — Configure environment variables

```bash
cp .env.example .env
```

Open `.env` and fill in your values:

```env
# Required
OPENAI_API_KEY=sk-...

# Optional — LLM model selection (defaults shown)
OPENAI_CHAT_MODEL=gpt-3.5-turbo
OPENAI_EMBEDDING_MODEL=text-embedding-3-small

# Optional — needed for Telegram integration
TELEGRAM_BOT_TOKEN=

# Optional — needed for Teams integration
TEAMS_APP_ID=
TEAMS_APP_PASSWORD=
```

### Step 3 — Start all services

```bash
docker-compose up --build
```

This starts:
- **Backend API** at `http://localhost:8000`
- **Admin UI** at `http://localhost:8501`

First startup takes ~60 seconds to build images and install dependencies.

### Step 4 — Open the Admin UI

Navigate to **http://localhost:8501** in your browser.

You should see the Dashboard with all metrics showing. The three default intent spaces (HR, Legal, Finance) are pre-created automatically.

### Step 5 — Upload sample documents

Three sample documents are included in `data/uploads/` — ready to use immediately:

| File | Intent Space | Format |
|------|-------------|--------|
| `1_hr_employee_handbook.pdf` | HR | PDF |
| `2_legal_data_privacy_policy.docx` | Legal | DOCX |
| `3_finance_q4_2025_report.pdf` | Finance | PDF |

To upload them:

1. Click **📂 KB Management** in the sidebar
2. Select one of the sample files above (or any PDF/DOCX, max 50MB)
3. Choose the matching intent space (HR / Legal / Finance)
4. Click **Upload & Parse**

The system will parse, chunk, embed, and index the document automatically. Status will show ✅ Processed when done.

### Step 6 — Send your first query

**Easiest way — use the built-in Chat UI:**

Navigate to **http://localhost:8501/Chat** in your browser.

- Set your **User ID** in the sidebar (e.g. `demo`)
- Click any sample question or type your own
- Each answer shows the detected intent, confidence score, response time, and source documents

Sample questions to try (matched to the uploaded documents):

| Question | Expected Intent | Source Document |
|----------|----------------|----------------|
| What is the annual leave policy? | HR | `1_hr_employee_handbook.pdf` |
| What personal data does the company collect? | Legal | `2_legal_data_privacy_policy.docx` |
| What was the revenue growth in Q4 2025? | Finance | `3_finance_q4_2025_report.pdf` |

**Or query via the REST API directly:**

The `user_id` field scopes query history per user. Use any string identifier (e.g. email, username, or `"demo"`).

```bash
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the annual leave policy?", "channel": "api", "user_id": "demo"}'
```

Each response includes `detected_intent`, `confidence`, `answer`, and `source_documents`.

Or browse all endpoints via the interactive API docs at **http://localhost:8000/docs**.

---

## Frontend Integration Setup

### Telegram Bot

**Step 1** — Create a bot via [@BotFather](https://t.me/botfather) on Telegram:
```
/newbot
→ Enter a name: IntelliKnow KMS
→ Enter a username: intelliknow_bot
→ Copy the token: 1234567890:ABCdef...
```

**Step 2** — Add the token to `.env`:
```env
TELEGRAM_BOT_TOKEN=1234567890:ABCdef...
```

**Step 3** — Restart the backend:
```bash
docker-compose restart backend
```

**Step 4** — Verify in Admin UI:
- Go to **🔗 Integrations** → Telegram should show 🟢 Connected
- Click **Test Connection** to verify

**Step 5** — Start chatting:
- Open your bot on Telegram
- Send `/start` for usage instructions
- Send any question: _"What is the reimbursement process?"_

---

### Microsoft Teams Bot (Local Testing with Bot Framework Emulator)

**Step 1** — Download [Bot Framework Emulator](https://aka.ms/botframework-emulator)

**Step 2** — Register the bot in Azure (skip App ID/Password for emulator testing):

For local emulator testing, App ID and Password can be left empty.

**Step 3** — Configure in Admin UI:
- Go to **🔗 Integrations** → Configure Microsoft Teams
- Enter App ID and App Password (can leave empty for emulator)

**Step 4** — Connect the emulator:
- Open Bot Framework Emulator
- Click **Open Bot**
- Enter URL: `http://localhost:8000/api/integrations/teams/messages`
- Click **Connect**

**Step 5** — Send a message in the emulator to test.

---

## Admin UI Guide

| Page | URL | Purpose |
|------|-----|---------|
| Dashboard | http://localhost:8501 | Overview metrics + recent queries |
| KB Management | http://localhost:8501/KB_Management | Upload/manage documents |
| Intent Config | http://localhost:8501/Intent_Config | Manage intent spaces + view query log |
| Integrations | http://localhost:8501/Integrations | Configure and test Telegram / Teams |
| Analytics | http://localhost:8501/Analytics | Query history, stats, CSV export |

### KB Management

- **Upload**: Drag and drop or browse for a PDF/DOCX file, select intent space, click Upload
- **Filter**: Filter documents by intent space or search by name
- **Delete**: Click 🗑️ then confirm to remove a document and its vectors

### Intent Configuration

- **Default spaces**: HR, Legal, Finance — cannot be deleted
- **Custom spaces**: Click **➕ Add New Intent Space**, enter name + keywords
- **Keywords**: Adding keywords improves classification accuracy for that space
- **Query log**: See every query's detected intent and confidence score

### Analytics

- **Intent distribution**: Bar chart showing query volume per intent space
- **Top documents**: Most-accessed documents by retrieval count
- **Export**: Download full query history as CSV

---

## API Documentation

Interactive API docs (Swagger UI): **http://localhost:8000/docs**

Full REST API specification: [`architecture/api-contract.md`](architecture/api-contract.md)

Key endpoints:

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/api/health` | Service health check |
| `POST` | `/api/documents` | Upload and parse a document |
| `GET` | `/api/documents` | List all documents |
| `DELETE` | `/api/documents/{id}` | Delete a document |
| `GET` | `/api/intents` | List intent spaces |
| `POST` | `/api/intents` | Create a new intent space |
| `POST` | `/api/query` | Submit a query (returns answer + citation) |
| `GET` | `/api/integrations` | Get integration status |
| `PUT` | `/api/integrations/telegram` | Configure Telegram |
| `GET` | `/api/analytics/queries` | Query history |
| `GET` | `/api/analytics/export` | Export logs as CSV |

---

## End-to-End Demo Flow

Follow these steps to verify the complete system works:

1. **Upload a document**
   - Admin UI → KB Management → upload `1_hr_employee_handbook.pdf` → select "HR" intent space → Upload & Parse
   - Verify status shows ✅ Processed

2. **Query via API**
   ```bash
   curl -X POST http://localhost:8000/api/query \
     -H "Content-Type: application/json" \
     -d '{"query": "What is the annual leave policy?", "channel": "api", "user_id": "demo"}'
   ```
   Expected: response with `detected_intent: "HR"`, `source_documents: ["1_hr_employee_handbook.pdf"]`

3. **Query via Telegram** (requires bot token configured)
   - Send _"What is the annual leave policy?"_ to your bot
   - Expected reply within 3 seconds with answer + 📄 Source citation

4. **Check the query log**
   - Admin UI → Analytics → see the query with intent, confidence score, and response time

---

## Stopping the Services

```bash
# Stop all containers
docker-compose down

# Stop and remove data volumes (full reset)
docker-compose down -v
```

---

## Running Without Docker

If you prefer running locally without Docker:

**Backend:**
```bash
cd backend
python -m venv venv && source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp ../.env.example .env  # fill in OPENAI_API_KEY
uvicorn main:app --reload --port 8000
```

**Frontend (separate terminal):**
```bash
cd frontend
pip install -r requirements.txt
BACKEND_URL=http://localhost:8000/api streamlit run app.py
```

---

## Project Structure

```
mini-kms/
├── backend/                    # FastAPI backend
│   ├── main.py                 # App entry point
│   ├── src/
│   │   ├── api/                # Route handlers
│   │   ├── services/           # Business logic
│   │   ├── ml/                 # AI/ML pipeline (parser, embedder, FAISS, RAG)
│   │   ├── db/                 # SQLAlchemy models + database init
│   │   └── integrations/       # Telegram + Teams bot handlers
│   └── Dockerfile
├── frontend/                   # Streamlit Admin UI
│   ├── app.py                  # Dashboard (entry point)
│   ├── pages/                  # 4 additional pages
│   ├── utils/                  # API client + helpers
│   └── Dockerfile
├── architecture/               # Design documents
│   ├── HLD.md                  # High-level system design
│   ├── LLD.md                  # Low-level design + package structure
│   ├── api-contract.md         # Full REST API specification
│   ├── data-model.md           # SQLite schema
│   ├── algorithm-arch.md       # RAG + intent classification design
│   └── ui-wireframes.md        # Streamlit page wireframes
├── data/                       # Runtime data (created on first run)
│   ├── intelliknow.db          # SQLite database
│   ├── faiss/                  # FAISS index files per intent space
│   └── uploads/                # Uploaded document files
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## AI Usage

See [`AI-USAGE.md`](AI-USAGE.md) for how AI tools were used strategically during development.

---

## Known Limitations (MVP)

- No user authentication — Admin UI is open (assumes local intranet use)
- Document re-parsing after editing is P2 (not in MVP)
- Teams integration requires Bot Framework Emulator for local testing (no public URL)
- FAISS uses exact search (IndexFlatL2) — suitable for < 100 documents; upgrade to IVF index for production scale
