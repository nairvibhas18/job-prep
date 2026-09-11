"""Mark resume-bullet spans with **...** (renderer turns them into \\textbf)."""

from __future__ import annotations

import re

# Longest-first. Taken from bold spans on the SWE/MLE base PDFs, plus
# common new-project tools so gap-closing bullets get the same treatment.
PHRASES = (
    "Retrieval Augmented Generation",
    "Retrieval-Augmented Generation",
    "Statistical Recurrent Units",
    "surgical activation clamping",
    "inference-time intervention",
    "bias mitigation strategy",
    "SQL Window Functions",
    "Qwen-2.5-7B-Instruct",
    "TransformerLens",
    "GitHub Actions",
    "TypeScript CDK",
    "Pydantic AI",
    "BeautifulSoup",
    "prompt injection",
    "Co-first author",
    "MMLU benchmark",
    "under 3 seconds",
    "PyTorch/TensorFlow",
    "PyTorch/Tensorflow",
    "Pytorch/Tensorflow",
    "AWS Lambda",
    "NeurIPS 2025",
    "4-dimension",
    "46% faster",
    "105 Kotest",
    "Next.js",
    "MechInterp",
    "PostgreSQL",
    "TensorFlow",
    "Tensorflow",
    "scikit-learn",
    "FastAPI",
    "Streamlit",
    "Opacus",
    "Kotest",
    "Bedrock",
    "Kotlin",
    "Runpod",
    "PyTorch",
    "Pytorch",
    "Lambda",
    "Docker",
    "Python",
    "Vercel",
    "React",
    "LSTMs",
    "LoSeR",
    "NPGML",
    "LSTM",
    "JAX",
    "SQL",
    "ETL",
    "MCP",
    "S3",
    "C++",
)

# Frozen metrics from the base resumes (and close variants).
PHRASES_METRICS = (
    "75,000+",
    "12,600+",
    "10,000+",
    "2,400+",
    "277",
    "146",
    "105",
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
    phrases = list(PHRASES) + list(PHRASES_METRICS)
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
