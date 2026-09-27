"""Minimal OpenAI- and Anthropic-compatible JSON completions."""

from __future__ import annotations

import json
import os
import re
from pathlib import Path

import httpx


def read_prompt(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def complete_json(system: str, user: str, *, temperature: float = 0.3) -> dict:
    provider = _provider()
    if provider == "anthropic":
        raw = _anthropic(system, user, temperature=temperature)
    elif provider == "openai":
        raw = _openai(system, user, temperature=temperature)
    else:
        raise RuntimeError(
            "No LLM key found. Set ANTHROPIC_API_KEY or OPENAI_API_KEY, "
            "or pass --from-json after a Cursor agent writes result.json."
        )
    return parse_json_object(raw)


def _provider() -> str | None:
    if os.environ.get("ANTHROPIC_API_KEY"):
        return "anthropic"
    if os.environ.get("OPENAI_API_KEY"):
        return "openai"
    return None


def _anthropic(system: str, user: str, *, temperature: float) -> str:
    key = os.environ["ANTHROPIC_API_KEY"]
    model = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-4-5")
    with httpx.Client(timeout=180.0) as client:
        r = client.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            json={
                "model": model,
                "max_tokens": 8192,
                "temperature": temperature,
                "system": system,
                "messages": [{"role": "user", "content": user}],
            },
        )
        r.raise_for_status()
        data = r.json()
    parts = [b.get("text", "") for b in data.get("content", []) if b.get("type") == "text"]
    return "\n".join(parts)


def _openai(system: str, user: str, *, temperature: float) -> str:
    key = os.environ["OPENAI_API_KEY"]
    model = os.environ.get("OPENAI_MODEL", "gpt-4.1")
    base = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1").rstrip("/")
    with httpx.Client(timeout=180.0) as client:
        r = client.post(
            f"{base}/chat/completions",
            headers={"Authorization": f"Bearer {key}", "content-type": "application/json"},
            json={
                "model": model,
                "temperature": temperature,
                "response_format": {"type": "json_object"},
                "messages": [
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
            },
        )
        r.raise_for_status()
        data = r.json()
    return data["choices"][0]["message"]["content"]


def parse_json_object(raw: str) -> dict:
    text = raw.strip()
    fenced = re.search(r"```(?:json)?\s*(\{.*\})\s*```", text, re.DOTALL)
    if fenced:
        text = fenced.group(1)
    start, end = text.find("{"), text.rfind("}")
    if start == -1 or end == -1:
        raise ValueError("LLM did not return a JSON object.")
    return json.loads(text[start : end + 1])
