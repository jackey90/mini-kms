# IntelliKnow KMS — MVP Scope & Milestones

## 1. MVP Goal

Deliver a demonstrable IntelliKnow KMS within **7 calendar days** that achieves the following core objectives:
- Receive and answer enterprise knowledge queries via Telegram + Teams (2 channels)
- Support PDF / DOCX document auto-parsing to build a searchable knowledge base
- Route queries via intent classification to HR / Legal / Finance knowledge domains
- Allow Admin to manage documents, intent spaces, and view analytics via a web UI

---

## 2. MVP Feature Boundary (In Scope)

### P0 — Must Deliver (core demo path)

| Feature | Description |
|---------|-------------|
| Telegram Bot messaging | Bot Token config, receive messages, return RAG responses |
| PDF / DOCX upload & parsing | Admin UI upload → LangChain parse → FAISS vectorize → queryable |
| Intent classification routing | 3 default spaces (HR / Legal / Finance) + General fallback |
| RAG retrieval response | Semantic search + LLM generates cited answer |
| Admin KB Management page | Document list, upload, delete, status view |
| Admin Intent Configuration page | Intent space CRUD + query classification log |

### P1 — Should Deliver (complete demo)

| Feature | Description |
|---------|-------------|
| Microsoft Teams Bot | Bot Framework integration, messaging |
| Admin Dashboard home | 4 module status metric cards |
| Admin Frontend Integration page | Connection status + test button |
| Admin Analytics page | Query history table + KB usage stats |
| Data export | CSV export of query logs |

### P2 — Optional (if time allows)

| Feature | Description |
|---------|-------------|
| Document re-parsing | Re-trigger vectorization after document content update |
| Mobile responsive Admin UI | Desktop-first, mobile optional |
| Configurable intent confidence threshold | Adjust threshold in Admin UI (default 70% is sufficient) |

---

## 3. Non-Goals (out of MVP scope)

| Non-goal | Reason |
|----------|--------|
| User authentication / access control | MVP single-user scenario, time limited |
| Multi-tenant / multi-enterprise support | Out of 7-day scope |
| Cloud deployment | Local Docker Compose satisfies demo requirements |
| Third-party SSO (LDAP / SAML) | Out of MVP scope |
| Real-time streaming responses | Polling mode meets ≤3s requirement |
| Document version management | Only overwrite updates supported |
| Native mobile app | Web Admin UI is sufficient |
| Slack / WhatsApp integration | MVP only does Telegram + Teams |
| Model fine-tuning / custom embeddings | OpenAI API meets accuracy requirements |

---

## 4. Day 1-7 Milestone Plan

| Day | Milestone | Key Tasks | Deliverables |
|-----|-----------|-----------|-------------|
| **Day 1** | Architecture + project skeleton | Architecture design (HLD/LLD/API Contract/DB Schema); FastAPI project init; Streamlit app init; Docker Compose skeleton | `architecture/` docs; runnable empty project |
| **Day 2** | Document parsing pipeline | PDF/DOCX upload API; LangChain parsing; FAISS vectorization; document CRUD API | `POST /documents` working; documents searchable |
| **Day 3** | Intent classification + RAG | OpenAI zero-shot intent classification; FAISS semantic search; LLM response generation; query API | `POST /query` end-to-end working |
| **Day 4** | Telegram Bot | Telegram Bot Polling mode; message routing to query API; reply format adaptation | Telegram Bot receives questions and answers |
| **Day 5** | Admin UI core pages | Streamlit KB Management page; Intent Configuration page; API integration | Admin can upload docs and manage intent spaces |
| **Day 6** | Teams Bot + Analytics | Teams Bot Framework integration; Analytics page; Dashboard; Frontend Integration page | Both Bots working; Admin UI complete |
| **Day 7** | Integration testing + delivery | End-to-end integration; README; AI-USAGE.md; Demo validation; Docker Compose full test | Complete demonstrable system |

### Critical Path

```
DB Schema → Document Parsing → RAG Retrieval → Query API → Telegram Bot  (P0 core path)
                                                           ↘ Teams Bot    (P1)
                                          ↗ Admin UI (parallel, Day 5)
```

---

## 5. Dependencies & Risks

| Dependency/Risk | Description | Mitigation |
|-----------------|-------------|------------|
| OpenAI API Key | Requires valid OpenAI API Key | Prepare in advance, configure via .env |
| Teams Bot registration complexity | Azure Bot registration process may be time-consuming | Evaluate on Day 1; if it takes more than half a day, use Mock |
| Telegram Polling mode | Local demo doesn't need Webhook; Polling is simpler | Use Polling by default |
| LLM classification accuracy | Zero-shot may fall below 70% | Validate on Day 3; if insufficient, add intent keyword hints to prompt |
