# IntelliKnow KMS — Algorithm Architecture

## 1. Document Ingestion Pipeline

### Overview
PDF/DOCX → Text Chunks → Embeddings → FAISS Index

```
┌──────────────┐    ┌─────────────────┐    ┌─────────────────────────────┐
│  Uploaded    │    │  LangChain      │    │  RecursiveCharacter         │
│  PDF/DOCX    │───▶│  Loader         │───▶│  TextSplitter               │
│  file        │    │  (extract text) │    │  chunk_size=500, overlap=50 │
└──────────────┘    └─────────────────┘    └──────────┬──────────────────┘
                                                       │  List[str] chunks
                                                       ▼
                                           ┌───────────────────────────┐
                                           │  OpenAI Embeddings API    │
                                           │  text-embedding-3-small   │
                                           │  1536-dim float vectors   │
                                           └──────────┬────────────────┘
                                                       │  List[ndarray]
                                           ┌───────────▼────────────────┐
                                           │  FAISS IndexFlatL2         │
                                           │  Per intent-space index    │
                                           │  Persist to disk after add │
                                           └────────────────────────────┘
```

### Chunking Strategy
- **Splitter**: `RecursiveCharacterTextSplitter`
- **chunk_size**: 500 characters (balances context vs. precision)
- **chunk_overlap**: 50 characters (prevents losing context at boundaries)
- **Separators**: `["\n\n", "\n", ". ", " ", ""]` — tries paragraph → sentence → word

### Embedding Model
- **Model**: `text-embedding-3-small` (1536 dimensions)
- **Batch size**: 20 chunks per API call to avoid rate limits
- **Cost estimate**: ~$0.002 per 1M tokens — negligible for MVP

### FAISS Configuration
- **Index type**: `IndexFlatL2` (exact L2 distance, no approximation)
- **Justification**: MVP has < 100 documents; exact search is fast enough
- **Persistence**: After each document addition, index is saved to `data/faiss/intent_{id}.index`

---

## 2. Intent Classification

### Overview
User query → OpenAI zero-shot classification → intent space + confidence score

```
User Query: "What is the reimbursement process?"
        │
        ▼
┌───────────────────────────────────────────────────────────────────┐
│  SYSTEM PROMPT (built dynamically from DB):                        │
│                                                                     │
│  You are an intent classifier for an enterprise knowledge base.    │
│  Classify the user query into one of these intent spaces:          │
│                                                                     │
│  - HR: Human resources policies, employee handbook, ...            │
│    Keywords: HR, employee, leave, salary, policy                   │
│  - Legal: Contract templates, compliance policies, ...             │
│    Keywords: contract, compliance, legal, NDA                      │
│  - Finance: Expense reimbursement, budget policy, ...              │
│    Keywords: budget, expense, reimbursement                        │
│                                                                     │
│  Return JSON: {"intent": "<name>", "confidence": <0.0-1.0>}        │
│  If confidence < 0.7, set intent to "general".                     │
└───────────────────────────────────────────────────────────────────┘
        │
        ▼  gpt-3.5-turbo (max_tokens=100, temperature=0)
        │
        ▼
{"intent": "Finance", "confidence": 0.88}
```

### Confidence Threshold
- **Default**: 0.7 (configurable via environment variable `INTENT_CONFIDENCE_THRESHOLD`)
- **Below threshold**: route to `general` — search all intent spaces combined
- **Rationale**: 0.7 is the minimum specified in requirements (FR-03-3)

### Fallback Behavior
1. confidence < 0.7 → `general` routing → search merged FAISS index (all spaces)
2. FAISS results similarity score < 0.5 → "no relevant content" response
3. Knowledge base empty → "KB is empty" response

---

## 3. RAG Retrieval Pipeline

### Overview
Query → Embed → FAISS search → Assemble context → LLM generate → Cited response

```
User Query
    │
    ▼ OpenAI text-embedding-3-small (~0.2s)
Query Embedding (1536-dim vector)
    │
    ▼ FAISS IndexFlatL2.search(k=5)  (<50ms)
Top-5 chunks [with L2 distance scores]
    │
    ▼ Filter: distance > threshold (similarity < 0.5) → fallback
Relevant chunks (1-5 items)
    │
    ▼ Assemble context string:
    │   "Context:\n[chunk1]\n---\n[chunk2]\n..."
    │
    ▼ gpt-3.5-turbo (~1.5s)
┌─────────────────────────────────────────────────────────────────┐
│  SYSTEM: You are a helpful knowledge base assistant.            │
│  Answer ONLY based on the provided context.                     │
│  If the answer is not in the context, say so clearly.          │
│  Keep answers concise (≤200 words). Always cite source docs.   │
│                                                                  │
│  USER: {query}                                                   │
│                                                                  │
│  Context:                                                        │
│  {assembled_chunks}                                              │
│                                                                  │
│  Sources: {source_document_names}                               │
└─────────────────────────────────────────────────────────────────┘
    │
    ▼
Response text + source document list
    │
    ▼ Format for channel (Telegram / Teams / API)
Final response
```

### Similarity Scoring
FAISS returns L2 distance. Lower = more similar.
- L2 distance is converted to a similarity score: `similarity = 1 / (1 + distance)`
- Threshold: if best chunk's similarity < 0.5, treat as "no relevant content found"

### Top-K Selection
- Retrieve k=5 chunks; pass all to LLM context
- LLM is instructed to synthesize from all relevant chunks, not just the first

---

## 4. Response Formatting

Responses are formatted differently per channel:

**Telegram** (plain text + emoji):
```
{answer_text}

📄 Source: {filename1}, {filename2}
```

**Teams** (plain text; Adaptive Card format is optional P2):
```
{answer_text}

Source: {filename1}, {filename2}
```

**API** (raw — for Admin UI preview):
```json
{
  "answer": "...",
  "source_documents": ["filename1.pdf"]
}
```

---

## 5. Bot Integration Architecture

### Telegram (Polling)
```
TelegramBot.run_polling()
    │  (runs in background thread via asyncio)
    │
    ▼ on_message(update)
    ├── extract text + user_id
    ├── POST /api/query {query, channel="telegram", user_id}
    └── send reply via telegram.Bot.send_message()
```

No Webhook needed for local demo. `python-telegram-bot` v20 handles polling natively.

### Microsoft Teams (Bot Framework)
```
Teams Bot endpoint: POST /api/integrations/teams/messages
    │
    ▼ botbuilder-python processes Activity
    ├── extract text from activity.text
    ├── POST /api/query {query, channel="teams", user_id}
    └── return Activity reply
```

Local testing: Bot Framework Emulator connects to `http://localhost:8000/api/integrations/teams/messages`

---

## 6. Performance Budget

| Operation | Target | Typical |
|-----------|--------|---------|
| Intent classification | < 800ms | ~400-600ms |
| Query embedding | < 300ms | ~200ms |
| FAISS search (k=5, <100 docs) | < 50ms | <5ms |
| LLM response generation | < 2000ms | ~1200-1800ms |
| **Total end-to-end** | **≤ 3000ms** | **~2000-2500ms** |
| Document parsing (10MB PDF) | < 60s | ~5-15s |
| Embedding (50 chunks) | < 5s | ~2-3s |
