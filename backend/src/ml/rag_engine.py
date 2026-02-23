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
) -> tuple[str, list[str], str]:
    """Generate a RAG response from retrieved chunks.

    The system prompt includes channel-specific formatting instructions so
    the LLM natively produces output suited to Telegram (concise, plain text,
    emoji markers) or Teams (bullet points, bold headers, markdown tables).
    """
    if not chunks or all(c["similarity"] < 0.3 for c in chunks):
        answer = "I couldn't find relevant information in the knowledge base."
        return answer, [], _format_for_channel(answer, [], channel, fallback=True)

    context = "\n---\n".join(c["chunk_text"] for c in chunks)
    source_docs = list(dict.fromkeys(c["filename"] for c in chunks))

    client = OpenAI(api_key=settings.openai_api_key)

    format_hint = _CHANNEL_FORMAT_INSTRUCTIONS.get(channel, "")

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

    response = client.chat.completions.create(
        model=settings.openai_chat_model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
        max_tokens=400,
        temperature=0.1,
    )

    answer = response.choices[0].message.content.strip()
    formatted = _format_for_channel(answer, source_docs, channel, fallback=False)
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
