from openai import OpenAI
from src.config import settings

TELEGRAM_MAX_LENGTH = 4096

# Channel-aware prompt fragments instruct the LLM to generate output that
# already fits the target platform's native constraints, so we don't need
# a separate per-channel formatter after the fact.
_CHANNEL_FORMAT_INSTRUCTIONS = {
    "telegram": (
        "\n\nFormat requirements (Telegram):"
        "\n- Keep the total response under 3500 characters."
        "\n- Use plain text with minimal formatting."
        "\n- Use emoji sparingly for key points (📌 ✅ ⚠️)."
        "\n- Never use markdown tables; present data as simple line-by-line text."
        "\n- Put source citations on a single line at the end."
    ),
    "teams": (
        "\n\nFormat requirements (Microsoft Teams):"
        "\n- Use bullet points (•) for multi-point answers."
        "\n- Use **bold** for key terms and section headers."
        "\n- Use markdown tables when presenting structured or tabular data."
        "\n- Organize the response with clear sections if it covers multiple topics."
        "\n- Put source citations in a separate '**Sources:**' section at the end."
    ),
    "api": "",
}


def generate_response(
    query: str,
    chunks: list[dict],
    channel: str = "api",
    conversation_history: list[dict] | None = None,
) -> tuple[str, list[str], str]:
    """Generate a RAG response from retrieved chunks.

    conversation_history: list of {"role": "user"|"assistant", "content": str}
    in chronological order. Injected between the system prompt and the current
    user message so the LLM has context from prior turns.

    The system prompt includes channel-specific formatting instructions so
    the LLM natively produces output suited to Telegram (concise, plain text,
    emoji markers) or Teams (bullet points, bold headers, markdown tables).
    """
    no_kb_results = not chunks or all(c["similarity"] < 0.3 for c in chunks)

    # When there are no KB results AND no prior conversation, return early.
    # When there IS conversation history, still call the LLM so it can answer
    # meta-questions like "what did I just ask?" from the injected history.
    if no_kb_results and not conversation_history:
        answer = "I couldn't find relevant information in the knowledge base."
        return answer, [], _format_for_channel(answer, [], channel, fallback=True)

    client = OpenAI(api_key=settings.openai_api_key)
    format_hint = _CHANNEL_FORMAT_INSTRUCTIONS.get(channel, "")

    if no_kb_results:
        # Answer from conversation history only — no KB context available
        system_prompt = (
            "You are a helpful enterprise knowledge base assistant.\n"
            "No relevant documents were found for this query.\n"
            "You may answer based on the conversation history above if the question refers to it.\n"
            "If the question requires knowledge base content that is not available, say so clearly.\n"
            "Keep answers concise (under 200 words)."
            f"{format_hint}"
        )
        user_message = f"Question: {query}"
        source_docs = []
    else:
        context = "\n---\n".join(c["chunk_text"] for c in chunks)
        source_docs = list(dict.fromkeys(c["filename"] for c in chunks))
        system_prompt = (
            "You are a helpful enterprise knowledge base assistant.\n"
            "Answer questions using ONLY the provided context. Do not use any prior knowledge.\n"
            "If the context does not contain the answer, say "
            '"I couldn\'t find relevant information in the provided documents."\n'
            "Keep answers concise (under 200 words). Be factual and professional."
            f"{format_hint}"
        )
        user_message = f"""Question: {query}

Context:
{context}

Sources: {', '.join(source_docs)}"""

    messages: list[dict] = [{"role": "system", "content": system_prompt}]
    if conversation_history:
        messages.extend(conversation_history)
    messages.append({"role": "user", "content": user_message})

    response = client.chat.completions.create(
        model=settings.openai_chat_model,
        messages=messages,
        max_tokens=400,
        temperature=0.1,
    )

    answer = response.choices[0].message.content.strip()
    # history-only answers have no source docs but are not a hard fallback
    formatted = _format_for_channel(answer, source_docs, channel, fallback=no_kb_results)
    return answer, source_docs, formatted


def _format_for_channel(
    answer: str, sources: list[str], channel: str, fallback: bool
) -> str:
    """Post-process the LLM output for hard platform constraints."""
    if fallback or not sources:
        if channel == "telegram":
            return _enforce_telegram_limit(answer)
        return answer

    sources_str = ", ".join(sources)

    if channel == "telegram":
        text = f"{answer}\n\n📄 Sources: {sources_str}"
        return _enforce_telegram_limit(text)
    elif channel == "teams":
        return f"{answer}\n\n---\n**Sources:** {sources_str}"
    else:
        return f"{answer}\n\nSources: {sources_str}"


def _enforce_telegram_limit(text: str) -> str:
    """Truncate to Telegram's 4096-char limit at a clean sentence boundary."""
    if len(text) <= TELEGRAM_MAX_LENGTH:
        return text

    budget = TELEGRAM_MAX_LENGTH - 40  # reserve room for the truncation notice
    truncated = text[:budget]

    for sep in ("\n\n", "\n", ". ", " "):
        pos = truncated.rfind(sep)
        if pos > len(truncated) // 2:
            truncated = truncated[: pos + len(sep)]
            break

    return truncated.rstrip() + "\n\n⚠️ Response truncated due to length."
