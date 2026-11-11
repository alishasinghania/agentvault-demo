"""Shared OpenRouter client (OpenAI-compatible chat API)."""

from typing import Any, Dict, List, Optional

import httpx
from langchain.llms.base import LLM

from app.config import (
    OPENROUTER_API_KEY,
    OPENROUTER_APP_NAME,
    OPENROUTER_BASE_URL,
    OPENROUTER_MAX_TOKENS,
    OPENROUTER_MODEL,
    OPENROUTER_SITE_URL,
)


def _headers() -> Dict[str, str]:
    if not OPENROUTER_API_KEY or OPENROUTER_API_KEY.startswith("your-"):
        raise RuntimeError(
            "OPENROUTER_API_KEY is not set. "
            "Create a key at https://openrouter.ai/keys and add it to .env"
        )
    return {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": OPENROUTER_SITE_URL,
        "X-Title": OPENROUTER_APP_NAME,
    }


def chat(
    messages: List[Dict[str, Any]],
    system: Optional[str] = None,
    model: Optional[str] = None,
) -> str:
    """Chat completion via OpenRouter /chat/completions."""
    msgs: List[Dict[str, Any]] = []
    if system:
        msgs.append({"role": "system", "content": system})
    for m in messages:
        role = m.get("role", "user")
        content = m.get("content", "")
        if isinstance(content, list):
            content = str(content)
        if role in ("user", "assistant", "system"):
            msgs.append({"role": role, "content": str(content)})

    payload = {
        "model": model or OPENROUTER_MODEL,
        "messages": msgs,
        "max_tokens": OPENROUTER_MAX_TOKENS,
    }
    url = f"{OPENROUTER_BASE_URL.rstrip('/')}/chat/completions"

    try:
        with httpx.Client(timeout=120.0) as client:
            resp = client.post(url, json=payload, headers=_headers())
            if resp.status_code >= 400:
                raise RuntimeError(
                    f"OpenRouter error {resp.status_code}: {resp.text[:500]}"
                )
            data = resp.json()
            choices = data.get("choices") or []
            if not choices:
                return ""
            message = choices[0].get("message") or {}
            return message.get("content", "") or ""
    except httpx.ConnectError as e:
        raise RuntimeError(
            f"Cannot reach OpenRouter at {OPENROUTER_BASE_URL}. Check your network."
        ) from e


def complete(prompt: str, model: Optional[str] = None) -> str:
    """Single-prompt completion via OpenRouter chat API."""
    return chat([{"role": "user", "content": prompt}], model=model)


class OpenRouterLLM(LLM):
    """LangChain LLM wrapper around OpenRouter (for agents / CrewAI / chains)."""

    @property
    def _llm_type(self) -> str:
        return "openrouter"

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Any = None,
        **kwargs: Any,
    ) -> str:
        return complete(prompt)

    def invoke(self, input: Any, config: Any = None, **kwargs: Any) -> str:
        """Explicit invoke() so AITrace catalog sink `llm.invoke` matches."""
        if isinstance(input, str):
            text = input
        elif hasattr(input, "content"):
            text = str(getattr(input, "content"))
        else:
            text = str(input)
        return self._call(text)


def get_langchain_llm():
    """LangChain-compatible LLM for code agent, research crew, RAG."""
    return OpenRouterLLM()
