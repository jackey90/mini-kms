# Tech Lead (Gen AI Focus) Interview Project Specification - Knowledge Management System

## 1. Project Overview

This project evaluates your ability to **independently build a functional, production-ready small Knowledge Management System (KMS)** while leveraging smart tooling to accelerate development---aligning with the Tech Lead role's focus on efficiency, integration, and strategic resource use. This project mirrors real-world Gen AI KMS realities with a *specific, actionable scenario*.

**Specific Scenario**: Many enterprises struggle with fragmented information, inefficient knowledge retrieval, and siloed communication channels. You will build a **Gen AI-powered Knowledge Management System** that addresses three core pain points: 1) Seamless integration with common frontend communication tools (Telegram, WhatsApp, Microsoft Teams, etc.) to enable knowledge queries directly from user-facing platforms; 2) A backend capable of automatically building and updating a knowledge base from uploaded documents (e.g., PDFs, Word docs, Excel sheets); 3) An orchestrator module that categorizes user queries into predefined intent spaces (e.g., HR, Legal, Finance, Operations) to route queries to the relevant knowledge domain and ensure accurate, context-aware responses. Core design principles include: intuitive knowledge ingestion, reliable multi-frontend integration, precise query classification, and fast, relevant response delivery.

**Target Outcome (Specific & Measurable)**: Build a fully functional, deployed KMS where a user/admin can:
1. Configure and use the KMS via at least 2 common frontend tools (e.g., Telegram + Microsoft Teams)
2. Upload documents to automatically build/update the backend knowledge base (with support for at least 2 document formats)
3. Define and manage intent spaces (HR, Legal, Finance, etc.)
4. Submit queries via integrated frontends, which are categorized by the orchestrator into the correct intent space
5. Receive accurate, context-aware responses derived from the knowledge base
6. View query history, classification accuracy, and knowledge base analytics (e.g., most accessed documents, common intent spaces)

**Constraints**:
- Timeline: 7 calendar days (1 week) from kickoff.
- Solo Work: No external collaboration; use standard developer resources (AI tools, official docs, Stack Overflow).
- Scope: MVP-focused (1-person workload); prioritize core functions (multi-frontend integration, document-driven KB, query orchestration); no over-engineering.
- AI Guidance: Leverage AI for key tasks (document parsing, query classification, response generation); document your strategic usage (intent/impact, not tool names).

## 2. Visual Reference Guidance

Simplified UI/UX guidelines (focus on core functionality, no design expertise required):

1. **Admin Dashboard**: Modular layout with 4 key sections (Frontend Integration, KB Management, Intent Configuration, Analytics) and clear navigation.
2. **KB Management**: Table for documents (name, date, format, status), prominent upload zone, basic search/filter.
3. **Intent Configuration**: Card view for intent spaces, log of queries/classification, simple edit form.
4. **Frontend Integration**: Status cards for each tool (connected/disconnected) with test button.

To align on expected UI/UX and functionality, below are *text-based visual guidelines* (no design expertise required---focus on usability and alignment with these cues):

1. **Admin Dashboard (Core UI)**:
   - Layout: Clean, modular dashboard with 4 key sections (all accessible via a top/side navigation menu): Frontend Integration, Knowledge Base Management, Intent Space Configuration, and Analytics.
   - Color Scheme: Soft, professional neutral base (white/light gray background) with distinct accent colors for each module (e.g., Frontend Integration = blue, Knowledge Base = green, Intent Space = purple).
   - Modular Design: Each section is a card with rounded corners (12px radius), padding (16px), and clear headings; avoid cluttered layouts---prioritize key actions (e.g., "Add Frontend Integration," "Upload Document," "Create Intent Space").

2. **Knowledge Base Management Interface**:
   - Document List: Table view with columns (Document Name, Upload Date, Format, Size, Status (Processed/Pending/Error), Actions (View/Delete/Update)).
   - Upload Area: Prominent drag-and-drop zone (or file picker button) with clear text indicating supported formats (PDF, DOCX recommended); progress indicator for document processing.
   - Search/Filter: Search bar to find documents by name/keyword; filter by format, upload date, or intent space association.

3. **Orchestrator & Intent Space Configuration**:
   - Intent Space List: Card view for each intent space (e.g., HR, Legal) with name, description, number of associated documents, and classification accuracy rate.
   - Query Classification Log: Table view showing recent queries, detected intent space, classification confidence score, and response status (Success/Failed).
   - Intent Space Editor: Simple form to create/edit intent spaces (name, description, keywords to improve classification accuracy).

4. **Frontend Integration Status**:
   - Integration Cards: One card per supported frontend tool (e.g., Telegram, Teams) with status indicator (Connected/Disconnected), configuration details (e.g., API Key last 4 digits), and test button (to send a sample query and verify integration).

## 3. Project Requirements (Non-Negotiable, Scenario-Specific)

You will build **"IntelliKnow KMS"**---a Gen AI-powered knowledge management system with multi-frontend integration, document-driven knowledge base, and query orchestration. All requirements are hyper-specific, actionable, and tied to the scenario above.

### 3.1 Functional Requirements (Core Modules)

- **Multi-Frontend Integration (Core)**:
  - Integrate 2 tools (Telegram/Teams/WhatsApp; prioritize accessible APIs).
  - Core Capabilities: Admin credential configuration (secure storage), real-time query/response sync (≤3s latency), status monitoring + error logging, end-to-end test function.
  - *Key Reference*: [Telegram Bot API](https://core.telegram.org/bots/api) | [Microsoft Teams Bot API](https://learn.microsoft.com/en-us/microsoftteams/platform/bots/how-to/create-a-bot-for-teams).

- **Document-Driven Backend KB (Core)**:
  - Support 2+ document formats (PDF, DOCX recommended).
  - Core Capabilities: AI-powered parsing/structuring of content, intent space association, manual updates + re-parsing, semantic search, basic error handling.
  - *Key Reference*: [LangChain Document Loaders](https://python.langchain.com/docs/modules/data_connection/document_loaders/) | [Lightweight KB Storage](https://www.sqlite.org/docs.html).

- **Orchestrator (Query Intent Classification, Core)**:
  - Intent Management: 3 default spaces (HR, Legal, Finance) + custom add/edit/delete.
  - Classification Logic: AI-powered (≥70% configurable confidence), fallback to "General" space, admin-guided accuracy improvement.
  - Core Capability: Route queries to relevant KB domains post-classification.
  - *Key Reference*: [AI Intent Classification Best Practices](https://product.hubspot.com/blog/ai-conversation-design-best-practices).

- **Knowledge Retrieval & Response**:
  - Generate concise, cited responses from KB; adapt format to frontend tools; clear "no match" messaging.

- **Admin UI/UX**:
  - 5 core screens (Dashboard, Frontend Integration, KB Management, Intent Configuration, Analytics); clean, intuitive, mobile-responsive (optional).
  - *Key Reference*: KMS Admin UI Inspiration.

- **Analytics & History**:
  - Log queries + metrics (timestamp, intent, confidence, response); track KB usage; exportable data.

> **Tech Stack (Simplified, Speed-Focused)**:
> - Option A (Recommended): Python (FastAPI/Streamlit) + SQLite/FAISS + AI tools.
> - Option B: JS (Next.js + Express.js) + SQLite/FAISS.
> - Prohibition: Complex frameworks/cloud services; lightweight only.
>
> *Key Reference*: [FastAPI](https://fastapi.tiangolo.com/tutorial/first-steps/) | [Streamlit](https://docs.streamlit.io/get-started) | [FAISS](https://github.com/facebookresearch/faiss/wiki/Getting-started).

### 3.2 AI Usage Reflection

- Key moments you turned to AI tools (e.g., overcoming document parsing challenges, improving query classification accuracy).
- How AI helped you iterate faster (e.g., streamlining parsing code, optimizing classification logic).
- Adjustments to AI outputs (e.g., refining parsed content, tuning classification thresholds).

**AI Usage Scenario Examples (2 Specific)**:
1. **Document Parsing**: When parsing PDF documents with embedded tables (e.g., HR salary grids), AI was used to extract structured tabular data and map it to relevant KB segments---solving the limitation of pure text parsing and ensuring numerical/structured knowledge was searchable, reducing manual data entry time by 60%.
2. **Frontend Integration**: AI was leveraged to adapt KMS responses to the native format constraints of each frontend tool (e.g., truncating long responses for Telegram, formatting bullet points for Teams)---ensuring consistent user experience across platforms without building custom formatters for each tool, streamlining integration development.

### 3.3 Delivery Requirements

- Public GitHub repo (code, docs, AI Usage Reflection).
- Working demo (deployed/local) with 2 frontend integrations, 2+ sample docs, testable query flow.
- Detailed README (setup, tech stack, integration guide).
- *Key Reference*: [Render](https://render.com/) | [Vercel](https://vercel.com/) | [GitHub Markdown](https://docs.github.com/en/get-started/writing-on-github/basic-writing-and-formatting-syntax).
