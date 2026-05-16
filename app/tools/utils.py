import openai
from app.config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

INTENT_LABELS = ["rag_query", "code_execution", "research", "database_query", "email", "general"]


def quick_classify(text: str) -> str:
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        f"Classify the user's intent into exactly one of: {', '.join(INTENT_LABELS)}. "
                        f"Return only the label, nothing else."
                    ),
                },
                {
                    "role": "user",
                    "content": f"Classify this request: {text}",
                },
            ],
            max_tokens=10,
            temperature=0,
        )
        label = response.choices[0].message.content.strip().lower()
        return label if label in INTENT_LABELS else "general"
    except Exception:
        return _heuristic_classify(text)


def _heuristic_classify(text: str) -> str:
    text_lower = text.lower()
    if any(w in text_lower for w in ["email", "send", "message", "notify"]):
        return "email"
    if any(w in text_lower for w in ["run", "execute", "python", "code", "calculate", "compute"]):
        return "code_execution"
    if any(w in text_lower for w in ["research", "find out", "investigate", "look into"]):
        return "research"
    if any(w in text_lower for w in ["database", "employees", "records", "query", "sql"]):
        return "database_query"
    if any(w in text_lower for w in ["policy", "handbook", "guideline", "procedure"]):
        return "rag_query"
    return "general"


def sanitize_for_logging(text: str) -> str:
    import re
    text = re.sub(r"sk-[a-zA-Z0-9]{20,}", "[REDACTED_KEY]", text)
    text = re.sub(r"password['\"]?\s*[:=]\s*['\"]?[^\s'\"]+", "password=[REDACTED]", text, flags=re.IGNORECASE)
    return text
