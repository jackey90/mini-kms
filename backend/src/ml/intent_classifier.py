import json
from openai import OpenAI
from src.config import settings


def classify_intent(
    query: str,
    intent_spaces: list[dict],
) -> tuple[str, float]:
    """Classify user query into an intent space using GPT zero-shot.

    Args:
        query: The user's question.
        intent_spaces: List of dicts with keys: name, description, keywords (list[str]).

    Returns:
        Tuple of (intent_name, confidence). intent_name is "general" if confidence
        is below the configured threshold.
    """
    client = OpenAI(api_key=settings.openai_api_key)

    spaces_text = "\n".join(
        f"- {s['name']}: {s['description']}. Keywords: {', '.join(s['keywords'])}"
        for s in intent_spaces
    )

    system_prompt = f"""You are an intent classifier for an enterprise knowledge base.
Classify the user query into exactly one of these intent spaces:

{spaces_text}

Respond with valid JSON only (no markdown, no explanation):
{{"intent": "<space_name>", "confidence": <0.0 to 1.0>}}

Rules:
- confidence represents how certain you are (0.0 = no match, 1.0 = perfect match)
- If no intent clearly matches, still pick the closest one but set low confidence
- Use the exact name from the list above"""

    response = client.chat.completions.create(
        model=settings.openai_chat_model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query},
        ],
        max_tokens=100,
        temperature=0,
    )

    raw = response.choices[0].message.content.strip()
    try:
        result = json.loads(raw)
        intent = result.get("intent", "general")
        confidence = float(result.get("confidence", 0.0))
    except (json.JSONDecodeError, ValueError):
        intent = "general"
        confidence = 0.0

    # Apply threshold — fall back to "general" if below threshold
    if confidence < settings.intent_confidence_threshold:
        intent = "general"

    return intent, confidence
