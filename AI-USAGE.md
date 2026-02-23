# AI Usage Reflection — IntelliKnow KMS

## 1. Document Parsing: AI-Powered Table Extraction

**Challenge**: Standard PDF text extractors (PyPDF, pdfminer) treat embedded tables as flat text, destroying row/column structure. When HR salary grids or financial tables are ingested, the resulting chunks become unsearchable noise — e.g., cell values from different columns merge into the same line.

**How AI Was Used**:
- **Detection**: `pdfplumber` scans each PDF page for table regions and extracts raw cell data (rows × columns).
- **Structuring**: The raw cell matrix is sent to OpenAI (GPT-3.5-turbo) with a system prompt that instructs the model to identify header rows, infer column semantics, and output clean Markdown tables with descriptive labels.
- **Integration**: The structured Markdown tables are appended to the page text before chunking, so the vector store indexes them as searchable, context-preserving content.

**Before / After**:
| Aspect | Before (pure text) | After (AI-structured) |
|--------|--------------------|-----------------------|
| Salary grid query | Returns garbled fragments | Returns the correct salary band with grade/level context |
| Chunk quality | Numeric values mixed across columns | Each row preserved as a coherent unit |
| Manual effort | Would need manual CSV conversion | Fully automated at upload time |

**Adjustments Made**: Tuned `temperature=0` for the structuring call to guarantee deterministic, faithful reproduction of numerical values. Added a fallback path so parsing still succeeds (text-only) if table extraction fails.

**Code**: `backend/src/ml/document_parser.py` — `_extract_tables_from_pdf()` + `_structure_tables_with_ai()`

---

## 2. Frontend Integration: Channel-Aware Response Formatting

**Challenge**: Telegram and Microsoft Teams have very different rendering capabilities and constraints. Telegram limits messages to 4,096 characters and supports minimal markdown; Teams renders rich markdown with bold, bullet lists, and tables. Sending the same raw text to both channels leads to a degraded experience on at least one platform.

**How AI Was Used**:
- **Prompt-level adaptation**: Instead of building separate post-processing formatters for each channel, channel-specific formatting instructions are injected into the RAG system prompt. For Telegram, the LLM is told to keep output under 3,500 characters, use plain text with emoji markers, and avoid markdown tables. For Teams, it's instructed to use bullet points, bold headers, and markdown tables for structured data.
- **Hard-limit enforcement**: A post-processing layer enforces Telegram's 4,096-character hard limit with smart truncation at sentence boundaries, appending a truncation notice if needed.
- **Teams structure**: Teams responses include a horizontal rule and bold "Sources" section for clean visual separation.

**Before / After**:
| Aspect | Before | After |
|--------|--------|-------|
| Telegram long answer | Raw text exceeding 4,096 chars → API error / silent truncation | Smart truncation at sentence boundary + truncation notice |
| Telegram tables | Broken markdown table rendering | Reformatted as line-by-line text |
| Teams answer | Plain text, no visual hierarchy | Bullet points, bold headers, markdown tables |
| Development effort | Would need a custom formatter per channel | Single prompt variation + lightweight post-processing |

**Adjustments Made**: Initially tried pure post-processing (regex-based reformatting), but it was brittle and lost semantic meaning. Shifting the adaptation into the LLM prompt produced naturally formatted output that required minimal post-processing — only the hard character limit needed enforcement.

**Code**: `backend/src/ml/rag_engine.py` — `_CHANNEL_FORMAT_INSTRUCTIONS` + `_enforce_telegram_limit()`

---

## 3. Other AI-Assisted Development Moments

| Area | How AI Helped |
|------|---------------|
| **Intent Classification** | Used GPT-3.5-turbo zero-shot classification with a structured JSON output format. Iterated on the prompt to include intent keywords from admin config, improving classification accuracy for domain-specific queries. |
| **RAG Prompt Engineering** | Tested multiple system prompt variations to balance conciseness vs. completeness. Added explicit "do not use prior knowledge" guardrail after observing hallucinated answers during early testing. |
| **Architecture Design** | Leveraged AI to evaluate trade-offs between FAISS (local, zero-cost) vs. hosted vector DBs (Pinecone, Weaviate). Chose FAISS for MVP simplicity and zero external dependency. |
