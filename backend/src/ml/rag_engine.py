from openai import OpenAI
from src.config import settings


def generate_response(
    query: str,
    chunks: list[dict],
    channel: str = "api",
) -> tuple[str, list[str], str]:
    """Generate a RAG response from retrieved chunks.

    Args:
        query: The user's original question.
        chunks: List of chunk dicts from vector_store.search()
                Each has: {chunk_text, filename, similarity, ...}
        channel: "telegram", "teams", or "api"

    Returns:
        Tuple of (answer_text, source_documents, channel_formatted_response)
    """
    # No results or all below similarity threshold → fallback
    if not chunks or all(c["similarity"] < 0.3 for c in chunks):
        answer = "I couldn't find relevant information in the knowledge base."
        return answer, [], _format_for_channel(answer, [], channel, fallback=True)

    context = "\n---\n".join(c["chunk_text"] for c in chunks)
    source_docs = list(dict.fromkeys(c["filename"] for c in chunks))  # unique, ordered

    client = OpenAI(api_key=settings.openai_api_key)

    system_prompt = """You are a helpful enterprise knowledge base assistant.
Answer questions using ONLY the provided context. Do not use any prior knowledge.
If the context does not contain the answer, say "I couldn't find relevant information in the provided documents."
Keep answers concise (under 200 words). Be factual and professional."""

    user_message = f"""Question: {query}

Context:
{context}

Sources: {', '.join(source_docs)}"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
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
    """Format the response for a specific channel."""
    if fallback or not sources:
        return answer

    sources_str = ", ".join(sources)

    if channel == "telegram":
        return f"{answer}\n\n📄 Source: {sources_str}"
    elif channel == "teams":
        return f"{answer}\n\nSource: {sources_str}"
    else:
        return f"{answer}\n\nSource: {sources_str}"
