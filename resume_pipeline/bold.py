"""Mark resume-bullet spans with **...** (renderer turns them into \\textbf)."""

from __future__ import annotations

import re

# Longest-first. Common tools so bullets that forgot ** still bold key tech.
# Counts and percents are picked up by METRIC_RE, not a personal metric list.
PHRASES = (
    "Retrieval Augmented Generation",
    "Retrieval-Augmented Generation",
    "GitHub Actions",
    "PyTorch/TensorFlow",
    "PyTorch/Tensorflow",
    "Pytorch/Tensorflow",
    "AWS Lambda",
    "Pydantic AI",
    "PostgreSQL",
    "TensorFlow",
    "Tensorflow",
    "scikit-learn",
    "FastAPI",
    "Next.js",
    "PyTorch",
    "Pytorch",
    "Lambda",
    "Docker",
    "Python",
    "React",
    "Kotlin",
    "JAX",
    "SQL",
    "S3",
    "C++",
)

METRIC_RE = re.compile(
    r"~\d+(?:\.\d+)?%"
    r"|\d+(?:\.\d+)?%"
    r"|\d{1,3}(?:,\d{3})+\+?"
)


def apply_bold(text: str, extra: list[str] | tuple[str, ...] | None = None) -> str:
    """Wrap metrics and key tech in **...**. Leave bullets that already have **."""
    if not text or "**" in text:
        return text
    phrases = list(PHRASES)
    if extra:
        phrases.extend(p for p in extra if p and p not in phrases)
    phrases.sort(key=len, reverse=True)

    n = len(text)
    used = [False] * n
    spans: list[tuple[int, int]] = []

    def occupy(i: int, j: int) -> bool:
        if i < 0 or j > n or i >= j:
            return False
        if any(used[i:j]):
            return False
        if not _boundary(text, i, j):
            return False
        for k in range(i, j):
            used[k] = True
        spans.append((i, j))
        return True

    for phrase in phrases:
        start = 0
        while True:
            i = text.find(phrase, start)
            if i < 0:
                break
            occupy(i, i + len(phrase))
            start = i + 1

    for match in METRIC_RE.finditer(text):
        occupy(match.start(), match.end())

    if not spans:
        return text
    spans.sort()
    out: list[str] = []
    cursor = 0
    for i, j in spans:
        out.append(text[cursor:i])
        out.append("**")
        out.append(text[i:j])
        out.append("**")
        cursor = j
    out.append(text[cursor:])
    return "".join(out)


def strip_bold(text: str) -> str:
    return text.replace("**", "")


def _boundary(text: str, i: int, j: int) -> bool:
    if i > 0 and text[i - 1].isalnum():
        return False
    if j < len(text) and text[j].isalnum():
        return False
    return True
