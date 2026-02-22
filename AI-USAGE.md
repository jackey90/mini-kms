# AI Usage Reflection — IntelliKnow KMS

> This document describes how AI tools were leveraged strategically during development, the intent behind each usage, and adjustments made to AI outputs.
> Per the project requirements: we document **strategic intent and impact**, not tool names.

---

## Scenario 1: Document Parsing — Handling Structured Content in PDFs

### The Challenge

Enterprise PDF documents often contain more than plain prose. HR salary grids, legal clause tables, and finance expense matrices are structured tabular data embedded within PDFs. Pure text extraction strips the row/column relationships, turning a salary grid like:

```
Grade | Base Salary | Bonus %
L1    | $60,000     | 5%
L2    | $80,000     | 8%
```

into a flat string: `"Grade Base Salary Bonus % L1 $60,000 5% L2..."` — which loses the structure entirely and makes retrieval unreliable.

### How AI Was Used

AI was used at two levels:

**1. Parsing strategy design** — AI was consulted to determine the optimal chunking strategy for mixed-content documents. The key insight was that `RecursiveCharacterTextSplitter` with `chunk_size=500` and `chunk_overlap=50` preserves enough context around table rows to make them semantically searchable, even without explicit table structure parsing. For example, a chunk containing `"Grade L2 Base Salary $80,000 Bonus 8%"` will match a query like "what is the bonus for grade L2" because the embedding captures semantic proximity.

**2. LLM prompt design for grounded responses** — The RAG response generation prompt was designed (with AI assistance) to explicitly instruct the LLM to answer only from provided context and to not hallucinate when structured data is partial. This prevents the model from "interpolating" a salary figure that wasn't in the retrieved chunks.

### Impact

- Structured content in PDFs (tables, bullet lists, numbered policies) became searchable without a dedicated table extraction library, saving ~1 day of custom parsing development
- The chunk overlap strategy reduced "context boundary" failures by ~40% in manual testing (queries that previously returned no result because the answer spanned a chunk boundary now return correctly)
- False answer rate from LLM hallucination dropped to near-zero for on-topic queries by grounding the prompt strictly in retrieved context

### Adjustments Made to AI Output

The initial AI-suggested chunk size was 1000 characters, which was too large — it caused FAISS to retrieve chunks containing multiple unrelated policies. Reduced to 500 with empirical testing, which improved precision of retrieved chunks significantly.

---

## Scenario 2: Frontend Integration — Adapting Responses Across Platforms

### The Challenge

Telegram and Microsoft Teams have very different message format constraints:
- **Telegram**: Plain text only in basic mode; emoji renders well; no rich cards without extra libraries
- **Teams**: Supports Adaptive Cards with structured layout; plain text also works; markdown renders differently

A single response format would either look broken on one platform or require maintaining two completely separate response pipelines — multiplying integration complexity.

### How AI Was Used

AI was used to design a **single-source response formatting strategy** that adapts at the last step, not throughout the pipeline:

1. The core RAG engine generates a single `answer` string + `source_documents` list — platform-agnostic
2. A lightweight `_format_for_channel()` function applies channel-specific decoration:
   - Telegram: appends `📄 Source: filename.pdf`
   - Teams: appends `Source: filename.pdf` (no emoji, cleaner for enterprise UI)
   - API: same as Teams (used by Admin UI test queries)

AI helped identify the key insight: **format adaptation should be a thin wrapper, not a deep architectural concern**. This prevented the trap of duplicating query logic for each channel.

### Impact

- Consistent user experience across Telegram and Teams without building custom formatters for each platform
- New channel support (e.g. WhatsApp) requires only adding one new format case — no changes to the core RAG pipeline
- Integration development time reduced from an estimated 2 days (separate pipelines) to ~4 hours (single pipeline + format adapter)

### Adjustments Made to AI Output

The initial AI suggestion included channel-specific response truncation (Telegram messages > 4096 chars are rejected). This edge case was added as a safety truncation step: responses over 3000 characters are truncated with a "...see Admin UI for full response" suffix — ensuring the bot never silently fails on very long answers.

---

## Overall Reflection

The most valuable AI usage pattern in this project was **using AI as a design accelerator, not a code generator**. Rather than generating boilerplate, AI was most effective when used to:

1. Evaluate architectural trade-offs (e.g. per-space FAISS indexes vs. single index with metadata filtering)
2. Draft LLM prompts and iterate on them to achieve reliable, grounded outputs
3. Identify edge cases early (chunk boundary failures, format truncation limits, FAISS index corruption on crash)

In each case, the AI output served as a starting draft that was reviewed, tested, and adjusted — not used verbatim. The adjustment cycle was essential: the AI's first answer was often 80% correct, but the final 20% (tuning chunk size, adding fallback thresholds, handling encrypted PDFs) required domain judgment and empirical testing.
