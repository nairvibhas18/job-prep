"""Fill the locked LaTeX template. The model never writes the preamble."""

from __future__ import annotations

import re
from pathlib import Path


def _e(text: str) -> str:
    """Escape resume text; **span** → \\textbf, ~50% and <1% as math."""
    if not text:
        return ""
    parts = text.split("**")
    if len(parts) % 2 == 0:
        parts = [text.replace("**", "")]
    out: list[str] = []
    for i, part in enumerate(parts):
        escaped = _e_plain(part)
        if i % 2:
            out.append(r"\textbf{" + escaped + "}")
        else:
            out.append(escaped)
    return "".join(out)


def _e_plain(text: str) -> str:
    """Escape resume text; keep ~50% and <1% as LaTeX math."""
    if not text:
        return ""
    holds: list[str] = []

    def stash(latex: str) -> str:
        holds.append(latex)
        return f"\x00{len(holds) - 1}\x00"

    def sim(match: re.Match) -> str:
        rest = match.group(1)
        pct = r"\%" if match.group(2) else ""
        return stash(r"$\sim$" + rest + pct)

    tmp = re.sub(r"~(\d+(?:\.\d+)?)(%)?", sim, text)
    tmp = tmp.replace("<1%", stash(r"$<$1\%"))
    for a, b in [
        ("&", r"\&"),
        ("%", r"\%"),
        ("$", r"\$"),
        ("#", r"\#"),
        ("_", r"\_"),
        ("{", r"\{"),
        ("}", r"\}"),
        ("^", r"\textasciicircum{}"),
    ]:
        tmp = tmp.replace(a, b)
    for i, chunk in enumerate(holds):
        tmp = tmp.replace(f"\x00{i}\x00", chunk)
    return tmp


def render(profile: dict, tailored: dict, template: str) -> str:
    body = []
    body.append(_header(profile))
    body.append(_education(profile, tailored))
    body.append(_skills(tailored))
    body.append(_work(tailored))
    body.append(_projects(tailored))
    return template.replace("%%BODY%%", "\n".join(body))


def _header(profile: dict) -> str:
    return f"""\\begin{{center}}
    \\textbf{{\\Huge \\scshape {_e(profile["name"])}}} \\\\ \\vspace{{4pt}}
    \\small {_e(profile["phone"])} $|$ {{\\underline{{{_e(profile["email"])}}}}} $|$
    \\href{{{profile["linkedin_url"]}}}{{\\underline{{{_e(profile["linkedin"])}}}}} $|$
    \\href{{{profile["github_url"]}}}{{\\underline{{{_e(profile["github"])}}}}}
    \\vspace{{-4mm}}
\\end{{center}}
"""


def _education(profile: dict, tailored: dict) -> str:
    edu = profile["education"]
    coursework = tailored.get("coursework") or ""
    return f"""
\\section{{Education}}
  \\resumeSubHeadingListStart
    \\resumeSubheading
      {{{_e(edu["school"])}}}{{{_e(edu["graduation"])}}}
      {{{_e(edu["degrees"])}}}{{{_e(edu["gpa"])}}}

    \\addvspace{{4pt}}

    \\resumeSubSubheadingLeft
        {{\\small{{\\textbf{{\\underline{{Relevant Coursework:}}}}}}}}
        {{{{\\small{{{_e(coursework)}}}}}}}

        \\vspace{{-1mm}}

    \\resumeSubSubheadingLeft
        {{\\small{{\\textbf{{\\underline{{Leadership:}}}}}}}}
        {{{{\\small{{{_e(profile["leadership"])}}}}}}}

    \\vspace{{-3.5mm}}
  \\resumeSubHeadingListEnd
"""


def _skills(tailored: dict) -> str:
    s = tailored["skills"]
    return f"""
\\section{{Technical Skills}}
 \\begin{{itemize}}[leftmargin=0.15in, label={{}}]
    \\small{{\\item{{
     \\textbf{{Languages}}{{: {_e(s["languages"])}}} \\\\
     \\textbf{{Developer Tools}}{{: {_e(s["developer_tools"])}}} \\\\
     \\textbf{{Libraries/Frameworks}}{{: {_e(s["libraries"])}}}
    }}}}
    \\vspace{{-2mm}}
 \\end{{itemize}}
"""


def _entry(company: str, dates: str, title: str, location: str, bullets: list[str]) -> str:
    items = "\n".join(f"      \\resumeItem{{{_e(b)}}}" for b in bullets)
    return f"""
    \\resumeSubheading
      {{{_e(company)}}}{{{_e(dates)}}}
      {{{_e(title)}}}{{{_e(location)}}}
      \\resumeItemListStart
{items}
      \\resumeItemListEnd
"""


def _work(tailored: dict) -> str:
    chunks = [_entry(w["company"], w["dates"], w["title"], w["location"], w["bullets"]) for w in tailored["work"]]
    return (
        "\\section{Work Experience}\n  \\resumeSubHeadingListStart\n"
        + "\n".join(chunks)
        + "\n  \\vspace{-2mm}\n  \\resumeSubHeadingListEnd\n"
    )


def _projects(tailored: dict) -> str:
    chunks = [
        _entry(p["name"], p["dates"], p["role"], p["location"], p["bullets"])
        for p in tailored["projects"]
    ]
    np = tailored.get("new_project")
    if np and np.get("bullets"):
        chunks.append(
            _entry(
                np["name"],
                np.get("dates") or "Jan. 2026 -- Present",
                np.get("role") or "Independent Project",
                np.get("location") or "Remote",
                np["bullets"],
            )
        )
    return (
        "\\section{Projects and Research Experience}\n  \\resumeSubHeadingListStart\n"
        + "\n".join(chunks)
        + "\n  \\vspace{-2mm}\n  \\resumeSubHeadingListEnd\n"
    )


def write_review(path: Path, tailored: dict, warnings: list[str], url: str) -> None:
    lines = [
        f"# Review — {tailored.get('company', '')} / {tailored.get('role', '')}",
        "",
        f"Source: {url}",
        f"Base: `{tailored.get('base')}`",
        f"Target team: {tailored.get('target_team') or '(none)'}",
        f"Replaced bottom project: `{tailored.get('replaced_bottom_id')}`",
        "",
        "## Fit",
        tailored.get("fit_summary") or "",
        "",
        "## Keep / cut",
    ]
    for item in tailored.get("keep_cut") or []:
        lines.append(f"- `{item.get('id')}`: **{item.get('action')}** — {item.get('reason', '')}")
    np = tailored.get("new_project")
    lines += ["", "## New project (80-hour MVP)", ""]
    if np:
        lines.append(f"**{np.get('name')}**")
        lines.append("")
        lines.append(np.get("what_it_is") or "")
        lines.append("")
        lines.append(f"**MVP:** {np.get('mvp') or ''}")
        lines.append("")
        lines.append(f"**Off the resume:** {np.get('stretch_off_resume') or ''}")
    else:
        lines.append("Skipped — existing projects already cover the JD.")
    lines += ["", "## Keyword map"]
    for km in tailored.get("keyword_map") or []:
        lines.append(f"- `{km.get('keyword')}` → {km.get('where')}")
    if warnings:
        lines += ["", "## Warnings"]
        for w in warnings:
            lines.append(f"- {w}")
    lines += [
        "",
        "## Before you upload",
        "- If a new project is listed, confirm those metrics after you run the experiment (they are conservative estimates).",
        "- Confirm you can whiteboard every project on the page in an interview.",
        "- Skim the PDF: one page, Amazon still has 4 bullets, metrics/tech are bold (`\\textbf`, no leftover `**`).",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
