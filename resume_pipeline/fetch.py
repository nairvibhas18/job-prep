"""Fetch a job posting from a URL into plain text."""

from __future__ import annotations

import re
from urllib.parse import urlparse

import httpx

JINA = "https://r.jina.ai/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; resume-pipeline/1.0; +https://github.com/nairvibhas18)"
}


def slug_from_url(url: str) -> str:
    host = urlparse(url).netloc.replace("www.", "")
    path = urlparse(url).path.strip("/").replace("/", "-")
    raw = f"{host}-{path}" if path else host
    slug = re.sub(r"[^a-zA-Z0-9-]+", "-", raw).strip("-").lower()
    return slug[:80] or "job"


def resume_stem(company: str = "", role: str = "", fallback: str = "resume") -> str:
    """Filename stem for resumes/<stem>.tex — company + role, not the URL."""
    raw = f"{company} {role}".strip() or fallback
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", raw).strip("-").lower()
    return (slug[:80].rstrip("-") or fallback[:80] or "resume")


def fetch_job_text(url: str, timeout: float = 60.0) -> str:
    """Prefer Jina reader (JS-heavy ATS pages), then raw HTTP."""
    errors: list[str] = []
    with httpx.Client(timeout=timeout, follow_redirects=True, headers=HEADERS) as client:
        try:
            r = client.get(JINA + url)
            r.raise_for_status()
            text = r.text.strip()
            if len(text) > 400:
                return text
            errors.append(f"jina too short ({len(text)} chars)")
        except httpx.HTTPError as exc:
            errors.append(f"jina: {exc}")

        try:
            r = client.get(url)
            r.raise_for_status()
            text = _strip_html(r.text)
            if len(text) > 400:
                return text
            errors.append(f"direct too short ({len(text)} chars)")
        except httpx.HTTPError as exc:
            errors.append(f"direct: {exc}")

    raise RuntimeError(
        "Could not fetch job posting. Save the JD as a .txt file and pass --jd-file.\n"
        + "\n".join(errors)
    )


def _strip_html(html: str) -> str:
    html = re.sub(r"(?is)<script[^>]*>.*?</script>", " ", html)
    html = re.sub(r"(?is)<style[^>]*>.*?</style>", " ", html)
    html = re.sub(r"(?s)<[^>]+>", " ", html)
    html = re.sub(r"&nbsp;", " ", html)
    html = re.sub(r"&amp;", "&", html)
    html = re.sub(r"&#39;|&apos;", "'", html)
    html = re.sub(r"&quot;", '"', html)
    html = re.sub(r"\s+", " ", html)
    return html.strip()
