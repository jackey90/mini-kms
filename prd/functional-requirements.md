# IntelliKnow KMS — Functional Requirements

> Format: User story + feature points + notes
> Priority: P0 (must) / P1 (should) / P2 (optional)

---

## FR-01 Multi-Frontend Integration

**Target users**: Admin (configuration), End User (usage)

### FR-01-1: Telegram Bot Integration (P0)

**User Story**:
> As an employee, I want to send questions directly to a Bot in Telegram and receive answers from the enterprise knowledge base within 3 seconds, so I don't need to open any additional web pages.

**Feature Points**:
- Admin configures Telegram Bot Token on the Frontend Integration page
- Bot uses Polling mode to listen for messages (local demo, no Webhook needed)
- After receiving user message, calls query API (FR-03 + FR-04) to get the answer
- Formats and replies to user (plain text + source citation)
- Supports `/start` command returning usage instructions

**Telegram Response Format**:
```
[Answer content]

📄 Source: [document name]
```

---

### FR-01-2: Microsoft Teams Bot Integration (P1)

**User Story**:
> As an enterprise employee, I want to ask the Bot questions in Microsoft Teams and receive the same quality of knowledge base answers as Telegram.

**Feature Points**:
- Admin configures Teams App ID + App Password on the Frontend Integration page
- Uses Bot Framework SDK (`botbuilder-python`) to handle messages
- Local demo uses Bot Framework Emulator or ngrok for testing
- Messages routed to the same query API
- Response format adapted for Teams (Adaptive Card or plain text)

**Teams Response Format**:
```
[Answer content]

Source: [document name]
```

---

### FR-01-3: Connection Status Monitoring (P1)

**User Story**:
> As an Admin, I want to see the connection status of each integration on the Frontend Integration page so I can quickly identify configuration issues.

**Feature Points**:
- Each integration shows status: `Connected` / `Disconnected` / `Error`
- Shows timestamp of last successful message
- Configuration details displayed (last 4 digits of API Key — full key not shown)

---

### FR-01-4: Integration Test Function (P1)

**User Story**:
> As an Admin, I want to click a "Test" button to send a test message to a specified integration and verify the connection is working.

**Feature Points**:
- Test button triggers sending a preset test message ("Hello, this is a test message from IntelliKnow KMS")
- Shows test result (success/failure + response time)

---

## FR-02 Document-Driven Knowledge Base

**Target users**: Admin

### FR-02-1: PDF Upload & Parsing (P0)

**User Story**:
> As an Admin, I want to upload a PDF file and have the system automatically parse its content and add it to the knowledge base, so employee queries can be answered based on this document.

**Feature Points**:
- Supports drag-and-drop upload or file picker
- File size limit: ≤ 50MB
- Uses LangChain `PyPDFLoader` to parse text content (including pages with tables)
- Text chunking: `RecursiveCharacterTextSplitter` (chunk_size=500, chunk_overlap=50)
- Vectorization: OpenAI `text-embedding-3-small`, stored in FAISS index
- Metadata stored in SQLite (filename, upload time, status, intent space ID, chunk count)
- Processing status: `Pending` → `Processing` → `Processed` / `Error`
- UI shows processing progress indicator

---

### FR-02-2: DOCX Upload & Parsing (P0)

**User Story**:
> As an Admin, I want to upload a Word document (.docx) and have the system correctly extract text content and add it to the knowledge base.

**Feature Points**:
- Same as FR-02-1; uses LangChain `Docx2txtLoader` for parsing
- Supports DOCX with tables (extracted as plain text)

---

### FR-02-3: Intent Space Association (P0)

**User Story**:
> As an Admin, I want to specify which intent space (e.g. HR) a document belongs to when uploading, so HR-related queries only search HR documents.

**Feature Points**:
- Upload form includes intent space selection dropdown
- One document belongs to one intent space (MVP limitation)
- FAISS index partitioned by intent space (each space has its own index)
- Uploaded documents can be reassigned to another intent space (triggers re-indexing)

---

### FR-02-4: Document Deletion (P1)

**Feature Points**:
- Document list supports single-item deletion
- Deletion removes corresponding vectors from FAISS index
- Confirmation dialog to prevent accidental deletion

---

### FR-02-5: Document Re-parsing (P2)

**Feature Points**:
- Document list supports "Reparse" action
- Re-uploading a file with the same name overwrites the existing document and triggers re-parsing

---

### FR-02-6: Basic Error Handling (P0)

**Feature Points**:
- Unsupported format uploaded: returns clear error message ("Only PDF and DOCX are supported")
- Parsing failure (e.g. encrypted PDF): document status becomes `Error`, shows error reason
- File too large: validated before upload, exceeds limit shows immediate message

---

### FR-02-7: Document Search & Filter (P1)

**Feature Points**:
- Search by document name
- Filter by intent space
- Sort by upload date

---

## FR-03 Intent Space Orchestrator

**Target users**: Admin (configuration), system (auto-classification)

### FR-03-1: Default Intent Spaces (P0)

**Feature Points**:
- System creates 3 default intent spaces on initialization:
  - **HR**: HR policies, employee handbook, attendance, compensation, annual leave
  - **Legal**: contract templates, legal terms, compliance policies, NDAs
  - **Finance**: expense reimbursement process, budget policy, financial reports, procurement approval
- Each intent space has: name, description, keywords list (to assist classification)

---

### FR-03-2: Custom Intent Space CRUD (P1)

**User Story**:
> As an Admin, I want to create custom intent spaces (e.g. "Operations") to support more knowledge domains.

**Feature Points**:
- Create: name (required) + description (optional) + keywords (optional, comma-separated)
- Edit: modify name/description/keywords
- Delete: only allowed when no documents are associated

---

### FR-03-3: AI Intent Classification (P0)

**Feature Points**:
- When a user query arrives, uses `gpt-3.5-turbo` for zero-shot classification
- Prompt includes all intent space names + descriptions + keywords
- Returns: `{ "intent": "HR", "confidence": 0.85 }`
- Confidence threshold: ≥ 0.7 (default)
- Classification result written to query log (FR-06-1)

---

### FR-03-4: Fallback Routing (P0)

**Feature Points**:
- Confidence < 0.7: routes to `General` space (searches all documents)
- `General` is a system-reserved space that cannot be deleted
- Bot response states "No exact knowledge domain match found; the following is from the general knowledge base"

---

### FR-03-5: Post-Intent RAG Retrieval (P0)

**Feature Points**:
- After intent space is determined, executes semantic search in that space's FAISS index
- Retrieves Top-5 most relevant chunks
- Assembles chunks into context, passes to LLM to generate response

---

## FR-04 Knowledge Retrieval & Response

### FR-04-1: RAG Response with Citations (P0)

**User Story**:
> As an employee, I want the Bot's answer to include the source document name so I can verify the accuracy of the information.

**Feature Points**:
- Response format: concise answer (≤200 words) + source document name
- LLM prompt requirement: answer must be grounded in provided context, no hallucinations
- If context does not contain relevant information, explicitly states "No relevant information found in the knowledge base"

---

### FR-04-2: Multi-Frontend Response Format Adaptation (P1)

**Feature Points**:
- Telegram: plain text + emoji source marker (`📄 Source:`)
- Teams: Adaptive Card (title + content + source link) or plain text

---

### FR-04-3: No-Match Fallback Response (P0)

**Feature Points**:
- Knowledge base is empty: returns "Knowledge base is empty. Please ask admin to upload documents."
- Retrieval results have low relevance (similarity score < 0.5): returns "I couldn't find relevant information in the knowledge base."
- Bot maintains friendly tone; does not return raw error messages

---

## FR-05 Admin UI

> **Tech**: Streamlit (Python) — Option A recommended stack

### FR-05-1: Dashboard Home (P1)

**Feature Points**:
- 4 module status metric cards (Frontend Integration / KB Management / Intent Config / Analytics)
- Each card shows key stats (connection count / document count / intent space count / today's query count)
- Click card navigates to corresponding page
- Streamlit sidebar navigation

---

### FR-05-2: Frontend Integration Page (P1)

**Feature Points**:
- One status card per integration (Telegram / Teams)
- Status indicator: Connected (green) / Disconnected (gray) / Error (red)
- Config button: opens config form (enter Token/API Key — masked)
- Test button: sends test message
- Details: last 4 digits of Token, last active time

---

### FR-05-3: KB Management Page (P0)

**Feature Points**:

Document list (table view):
- Columns: document name / upload date / format / size / intent space / status / actions
- Status badge colors: Processed (green) / Processing (yellow) / Error (red) / Pending (gray)
- Actions: delete

Upload section:
- Streamlit `st.file_uploader` widget (PDF, DOCX)
- Intent space selector dropdown
- Upload progress indicator (`st.spinner`)
- Supported formats shown

Search + filter:
- Search box (by document name)
- Intent space dropdown filter

---

### FR-05-4: Intent Configuration Page (P0)

**Feature Points**:

Intent space list (card view):
- Per card: name / description / associated doc count / classification accuracy (last 7 days)
- Actions: edit / delete (delete disabled when documents are associated)
- "Add Intent Space" button

Query classification log (table):
- Columns: time / query (truncated 50 chars) / detected intent / confidence / response status
- Pagination (20 per page)

Intent edit form:
- Name (required) / description / keywords (comma-separated)
- Save / cancel

---

### FR-05-5: Analytics Page (P1)

**Feature Points**:
- Full query history list (time / intent / confidence / response status / source docs)
- KB usage stats: top 10 most accessed documents
- Query volume distribution per intent space
- Date range filter
- Export CSV button (`st.download_button`)

---

## FR-06 Analytics & History

### FR-06-1: Automatic Query Logging (P0)

**Feature Points**:
- Every query automatically written to SQLite `query_logs` table
- Logged fields: id / timestamp / user_query / detected_intent / confidence_score / source_documents / response_status / channel (telegram/teams)

---

### FR-06-2: KB Usage Tracking (P1)

**Feature Points**:
- Each time a document is retrieved (search hit), updates that document's `access_count` counter
- Analytics page shows document access popularity ranking

---

### FR-06-3: Data Export (P2)

**Feature Points**:
- `GET /api/analytics/export` returns query logs in CSV format
- Admin UI provides "Export CSV" button to trigger download
