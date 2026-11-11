INTENT_LABELS = ["rag_query", "code_execution", "research", "database_query", "email", "general"]


def quick_classify(text: str) -> str:
    """Heuristic intent classification (no OpenAI key required)."""
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
