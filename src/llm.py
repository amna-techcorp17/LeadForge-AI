from __future__ import annotations

import json
import os
from functools import lru_cache
from typing import Any

from dotenv import load_dotenv

load_dotenv()

_LLM_DISABLED = False


@lru_cache(maxsize=1)
def get_llm():
    global _LLM_DISABLED
    if _LLM_DISABLED:
        return None
    api_key = os.getenv("GROQ_API_KEY", "").strip()
    if not api_key or api_key == "your_api_key_here" or "your_real" in api_key:
        return None

    from langchain_groq import ChatGroq

    return ChatGroq(
        groq_api_key=api_key,
        model_name=os.getenv("GROQ_MODEL", "llama-3.1-8b-instant"),
        temperature=0.2,
    )


def parse_json_response(content: str, fallback: dict[str, Any]) -> dict[str, Any]:
    try:
        start = content.find("{")
        end = content.rfind("}") + 1
        if start >= 0 and end > start:
            return {**fallback, **json.loads(content[start:end])}
    except json.JSONDecodeError:
        pass
    return fallback


def invoke_json(prompt: str, fallback: dict[str, Any]) -> dict[str, Any]:
    global _LLM_DISABLED
    llm = get_llm()
    if llm is None:
        return fallback
    try:
        response = llm.invoke(prompt)
        content = getattr(response, "content", str(response))
        return parse_json_response(content, fallback)
    except Exception:
        _LLM_DISABLED = True
        return fallback
