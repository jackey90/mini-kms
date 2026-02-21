# IntelliKnow KMS — Acceptance Criteria

> Language: English (referenced directly by QA)
> Format: Given / When / Then
> Priority: P0 (must pass for release) / P1 (should pass) / P2 (nice to have)

---

## AC-FR01: Multi-Frontend Integration

### AC-FR01-1: Telegram Bot Basic Query (P0)
- **Given** a Telegram Bot Token is configured in the system
- **When** a user sends a natural language question to the Bot
- **Then** the Bot replies with a relevant answer within 3 seconds, and the reply includes the source document name

### AC-FR01-2: Telegram Bot Start Command (P1)
- **Given** the Telegram Bot is running
- **When** a user sends `/start`
- **Then** the Bot replies with a usage guide message

### AC-FR01-3: Teams Bot Basic Query (P1)
- **Given** a Teams Bot App ID and App Password are configured
- **When** a user sends a natural language question via Teams (or Bot Framework Emulator)
- **Then** the Bot replies with a relevant answer within 3 seconds

### AC-FR01-4: Integration Status Display (P1)
- **Given** the Admin Dashboard is open
- **When** a Bot Token is configured and the Bot is running
- **Then** the Frontend Integration page shows "Connected" status for that integration

### AC-FR01-5: Integration Test Button (P1)
- **Given** an integration is configured
- **When** Admin clicks the "Test" button
- **Then** a test message is sent to the channel and the test result (success/failure + response time) is displayed within 5 seconds

---

## AC-FR02: Document-Driven Knowledge Base

### AC-FR02-1: PDF Upload and Processing (P0)
- **Given** the Admin is on the KB Management page
- **When** Admin uploads a valid PDF file (≤ 50MB) and selects an intent space
- **Then** the document appears in the list with status "Processing", transitions to "Processed" within 60 seconds, and the document content becomes queryable

### AC-FR02-2: DOCX Upload and Processing (P0)
- **Given** the Admin is on the KB Management page
- **When** Admin uploads a valid DOCX file and selects an intent space
- **Then** the document is processed successfully (status "Processed") and its content is queryable

### AC-FR02-3: Unsupported Format Rejection (P0)
- **Given** the Admin attempts to upload a file
- **When** the file format is not PDF or DOCX (e.g., .txt, .xlsx)
- **Then** the upload is rejected immediately with the message "Only PDF and DOCX formats are supported"

### AC-FR02-4: Intent Space Association (P0)
- **Given** a document is uploaded with intent space "HR"
- **When** a user submits an HR-related query
- **Then** the retrieved answer is based on content from that document (not from Legal or Finance documents)

### AC-FR02-5: Document Deletion (P1)
- **Given** a document exists in the knowledge base
- **When** Admin clicks "Delete" and confirms
- **Then** the document is removed from the list and its content is no longer returned in query results

### AC-FR02-6: Large File Rejection (P1)
- **Given** Admin selects a file larger than 50MB
- **When** the upload is initiated
- **Then** the system rejects the upload before sending to server with message "File size exceeds 50MB limit"

---

## AC-FR03: Intent Space Orchestrator

### AC-FR03-1: Default Intent Spaces Exist (P0)
- **Given** the system has been freshly initialized
- **When** Admin opens the Intent Configuration page
- **Then** three default intent spaces are present: HR, Legal, and Finance

### AC-FR03-2: Intent Classification Accuracy (P0)
- **Given** documents have been uploaded to each intent space
- **When** 10 test queries are submitted (≥ 4 HR, ≥ 3 Legal, ≥ 3 Finance)
- **Then** at least 7 out of 10 queries (≥ 70%) are classified into the correct intent space

### AC-FR03-3: Low-Confidence Fallback (P0)
- **Given** a query is submitted that does not clearly match any intent space
- **When** the classification confidence score is below 0.7
- **Then** the query is routed to the "General" space and the Bot response indicates it is from the general knowledge base

### AC-FR03-4: Custom Intent Space Creation (P1)
- **Given** Admin is on the Intent Configuration page
- **When** Admin creates a new intent space with a name and description
- **Then** the new intent space appears in the list and is available for document association and query routing

### AC-FR03-5: Intent Space Deletion with Documents Blocked (P1)
- **Given** an intent space has associated documents
- **When** Admin attempts to delete that intent space
- **Then** the deletion is blocked with message "Cannot delete intent space with associated documents. Please reassign or delete documents first."

---

## AC-FR04: Knowledge Retrieval and Response

### AC-FR04-1: Response Includes Source Citation (P0)
- **Given** a document has been uploaded to the knowledge base
- **When** a user submits a query that matches the document content
- **Then** the Bot response includes the source document name as a citation

### AC-FR04-2: Empty Knowledge Base Response (P0)
- **Given** no documents have been uploaded to the knowledge base
- **When** a user submits any query
- **Then** the Bot responds with a clear message: "The knowledge base is empty. Please ask your administrator to upload documents."

### AC-FR04-3: No Match Response (P0)
- **Given** documents are uploaded but none are relevant to the query
- **When** a user submits a query with low semantic similarity to all documents
- **Then** the Bot responds with: "I couldn't find relevant information in the knowledge base for your question."

### AC-FR04-4: Response Conciseness (P1)
- **Given** a matching document exists
- **When** a query is processed
- **Then** the response body is ≤ 300 words and is written in clear, natural language

---

## AC-FR05: Admin UI

### AC-FR05-1: All Pages Accessible (P0)
- **Given** the Admin UI is running
- **When** Admin navigates to each page (Dashboard / KB Management / Intent Configuration / Frontend Integration / Analytics)
- **Then** all 5 pages load without errors (no blank pages, no 500 errors, no broken layouts)

### AC-FR05-2: KB Management Upload Flow (P0)
- **Given** Admin is on KB Management page
- **When** Admin drags and drops a PDF file onto the upload area and selects an intent space
- **Then** the file upload starts, a progress indicator is visible, and upon completion the document appears in the list

### AC-FR05-3: Intent Configuration Log (P1)
- **Given** queries have been submitted via a Bot
- **When** Admin opens the Intent Configuration page
- **Then** the query classification log shows entries with: timestamp, query text (truncated), detected intent, and confidence score

### AC-FR05-4: Document Search (P1)
- **Given** multiple documents are in the knowledge base
- **When** Admin types a keyword in the search box
- **Then** only documents with matching names are shown in the list

---

## AC-FR06: Analytics and History

### AC-FR06-1: Query Log Auto-Recording (P0)
- **Given** a Bot query is processed
- **When** Admin opens the Analytics page
- **Then** the query appears in the history log with: timestamp, query text, detected intent, confidence score, and response status

### AC-FR06-2: CSV Export (P2)
- **Given** query history exists
- **When** Admin clicks "Export CSV"
- **Then** a CSV file is downloaded containing all query log entries

---

## AC-NFR: Non-Functional Acceptance Criteria

### AC-NFR-01: End-to-End Response Time (P0)
- **Given** a Bot integration is configured and documents are in the knowledge base
- **When** a user sends a query via Telegram or Teams
- **Then** the Bot reply is received within 3 seconds (measured from message sent to reply received)

### AC-NFR-02: Docker Compose Startup (P0)
- **Given** a clean environment with Docker and valid `.env` configured
- **When** `docker-compose up` is run
- **Then** all services are healthy and accessible within 30 seconds

### AC-NFR-03: Data Persistence on Restart (P0)
- **Given** documents have been uploaded and queries have been made
- **When** `docker-compose restart` is run
- **Then** all documents and query logs are still present after restart

### AC-NFR-04: Sensitive Keys Not Exposed (P0)
- **Given** the Admin UI is open on the Frontend Integration page
- **When** a configured Bot Token is displayed
- **Then** only the last 4 characters of the token are visible (e.g., "****3a9f")

### AC-NFR-05: Concurrent Query Handling (P1)
- **Given** the system is running
- **When** 5 queries are submitted simultaneously
- **Then** all 5 receive correct responses within 5 seconds with no errors
