"""Fetch a job posting and render JSON → locked LaTeX. The Cursor agent is the writer."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from dotenv import load_dotenv

from resume_pipeline.fetch import fetch_job_text, resume_stem, slug_from_url
from resume_pipeline.finalize import finalize, load_base, warnings_for
from resume_pipeline.render import render

ROOT = Path(__file__).resolve().parent
WORK = ROOT / "work"
RESUMES = ROOT / "resumes"


def main(argv: list[str] | None = None) -> int:
    load_dotenv(ROOT / ".env")
    p = argparse.ArgumentParser(
        description=(
            "Prepare a job folder or render result.json to LaTeX. "
            "Default: no external LLM — the Cursor agent writes result.json. "
            "User-facing output is resumes/<company>-<role>.tex and .pdf only."
        )
    )
    p.add_argument("urls", nargs="*", help="Job posting URL(s)")
    p.add_argument("--jd-file", type=Path, help="Plain-text JD instead of fetching a URL")
    p.add_argument("--team", default="", help="Target team override (wins over generic JD)")
    p.add_argument("--base", choices=["auto", "swe", "mle"], default="auto")
    p.add_argument("--from-json", type=Path, help="Finalize + render this result.json")
    p.add_argument("--work", type=Path, default=WORK, help="Scratch dir (jd.md, result.json)")
    p.add_argument("--resumes", type=Path, default=RESUMES, help="Deliverable dir (tex + pdf)")
    p.add_argument("--slug", default="", help="Scratch folder name under --work")
    p.add_argument(
        "--pdf",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Compile PDF into resumes/ (default: yes). Use --no-pdf to skip.",
    )
    p.add_argument(
        "--llm",
        action="store_true",
        help="Opt-in: call Anthropic/OpenAI instead of the Cursor agent",
    )
    p.add_argument("--skip-critic", action="store_true", help="With --llm, skip the critic pass")
    args = p.parse_args(argv)

    if args.from_json:
        return _render_from_json(args.from_json, args)

    if args.jd_file:
        jd = args.jd_file.read_text(encoding="utf-8")
        url = str(args.jd_file)
        slug = args.slug or args.jd_file.stem
        return _run_one(url, jd, slug, args)

    if not args.urls:
        p.error("Pass a job URL, --jd-file, or --from-json")

    code = 0
    for url in args.urls:
        try:
            print(f"Fetching {url} ...", flush=True)
            jd = fetch_job_text(url)
            slug = args.slug or slug_from_url(url)
            code = max(code, _run_one(url, jd, slug, args))
        except Exception as exc:
            print(f"ERROR {url}: {exc}", file=sys.stderr)
            code = 1
    return code


def _run_one(url: str, jd: str, slug: str, args) -> int:
    dest = args.work / slug
    dest.mkdir(parents=True, exist_ok=True)
    (dest / "jd.md").write_text(jd, encoding="utf-8")
    (dest / "url.txt").write_text(url + "\n", encoding="utf-8")

    if args.llm:
        return _run_external_llm(url, jd, dest, args)

    result_path = dest / "result.json"
    if result_path.exists():
        print(f"Found {result_path}; finalizing and rendering.")
        return _render_from_json(result_path, args)

    print(f"Prepared {dest / 'jd.md'}")
    print("Cursor agent: write work/<slug>/result.json, then render.")
    print(f"  1. Read prompts/writer.md, prompts/examples.md, prompts/critic.md")
    print(f"  2. Read {dest / 'jd.md'} and data/base_swe.json, data/base_mle.json")
    print(f"  3. Write {result_path} (JSON only, no markdown fence)")
    print(f"  4. python tailor.py --from-json {result_path}")
    return 0


def _run_external_llm(url: str, jd: str, dest: Path, args) -> int:
    from resume_pipeline.llm import complete_json, read_prompt

    system = read_prompt(ROOT / "prompts" / "writer.md") + "\n\n" + read_prompt(ROOT / "prompts" / "examples.md")
    user = _user_prompt(jd, args)
    print("Calling external writer LLM (--llm) ...", flush=True)
    draft = complete_json(system, user)
    if not args.skip_critic:
        try:
            print("Calling external critic LLM ...", flush=True)
            draft = complete_json(
                read_prompt(ROOT / "prompts" / "critic.md"),
                json.dumps(draft),
                temperature=0.1,
            )
        except Exception as exc:
            print(f"Critic skipped: {exc}", file=sys.stderr)
    (dest / "result.json").write_text(json.dumps(draft, indent=2), encoding="utf-8")
    return _render_from_json(dest / "result.json", args)


def _render_from_json(result_path: Path, args) -> int:
    draft = json.loads(result_path.read_text(encoding="utf-8"))
    slug = args.slug or result_path.parent.name
    work_dest = args.work / slug
    work_dest.mkdir(parents=True, exist_ok=True)

    jd = _load_jd(result_path, work_dest)
    team = args.team or draft.get("target_team") or ""
    if args.team:
        draft["target_team"] = args.team

    base_name = draft.get("base") if args.base == "auto" else args.base
    if base_name not in ("swe", "mle"):
        base_name = "mle" if _looks_ml(jd, team) else "swe"
        draft["base"] = base_name

    base = load_base(ROOT, base_name)
    ml_role = base_name == "mle" or _looks_ml(jd, team)
    tailored = finalize(base, draft, ml_role=ml_role)
    (work_dest / "result.json").write_text(json.dumps(tailored, indent=2), encoding="utf-8")
    if result_path.resolve() != (work_dest / "result.json").resolve():
        result_path.write_text(json.dumps(tailored, indent=2), encoding="utf-8")

    profile = json.loads((ROOT / "data" / "profile.json").read_text(encoding="utf-8"))
    template = (ROOT / "templates" / "resume.tex").read_text(encoding="utf-8")
    tex = render(profile, tailored, template)

    args.resumes.mkdir(parents=True, exist_ok=True)
    stem = resume_stem(tailored.get("company") or "", tailored.get("role") or "", slug)
    tex_path = args.resumes / f"{stem}.tex"
    tex_path.write_text(tex, encoding="utf-8")
    print(f"Wrote {tex_path}")

    for warning in warnings_for(tailored):
        print(f"WARNING: {warning}", file=sys.stderr)

    if args.pdf:
        pdf_path = _pdf(tex_path)
        if pdf_path:
            print(f"Wrote {pdf_path}")
    return 0


def _load_jd(result_path: Path, work_dest: Path) -> str:
    for candidate in (result_path.parent / "jd.md", work_dest / "jd.md"):
        if candidate.exists():
            if candidate.resolve() != (work_dest / "jd.md").resolve():
                work_dest.mkdir(parents=True, exist_ok=True)
                shutil.copy2(candidate, work_dest / "jd.md")
            return candidate.read_text(encoding="utf-8")
    return ""


def _user_prompt(jd: str, args) -> str:
    profile = (ROOT / "data" / "profile.json").read_text(encoding="utf-8")
    swe = (ROOT / "data" / "base_swe.json").read_text(encoding="utf-8")
    mle = (ROOT / "data" / "base_mle.json").read_text(encoding="utf-8")
    team = args.team or "(none — infer from JD)"
    return f"""Target team: {team}
Requested base: {args.base}

## Job posting
{jd[:24000]}

## Profile
{profile}

## SWE base resume JSON
{swe}

## MLE base resume JSON
{mle}
"""


def _looks_ml(jd: str, team: str) -> bool:
    blob = f"{team}\n{jd}".lower()
    hits = (
        "machine learning",
        "ml intern",
        "mle",
        "research intern",
        "deep learning",
        "pytorch",
        "llm",
        "ai intern",
        "ai engineer",
    )
    swe_hits = ("software development intern", "sde intern", "software engineer intern")
    if any(h in blob for h in swe_hits) and "machine learning" not in blob:
        if team and any(x in team.lower() for x in ("ml", "runtime", "learning", "pytorch")):
            return True
        return False
    return sum(h in blob for h in hits) >= 1


def _pdf(tex_path: Path) -> Path | None:
    """Compile in a temp dir so .aux/.log never land in resumes/."""
    pdf_dest = tex_path.with_suffix(".pdf")
    env = os.environ.copy()
    texbin = Path("/Library/TeX/texbin")
    if texbin.is_dir():
        env["PATH"] = f"{texbin}{os.pathsep}{env.get('PATH', '')}"
    with tempfile.TemporaryDirectory(prefix="resume-latex-") as tmp:
        tmp_path = Path(tmp)
        tmp_tex = tmp_path / "resume.tex"
        shutil.copy2(tex_path, tmp_tex)
        cmd = ["latexmk", "-pdf", "-interaction=nonstopmode", "-f", tmp_tex.name]
        try:
            subprocess.run(cmd, cwd=tmp_path, check=False, env=env, capture_output=True)
        except FileNotFoundError:
            print("latexmk not found; skip PDF (install MacTeX / TeX Live).", file=sys.stderr)
            return None
        built = tmp_path / "resume.pdf"
        if not built.exists():
            print("latexmk did not produce a PDF.", file=sys.stderr)
            return None
        shutil.copy2(built, pdf_dest)
    return pdf_dest


if __name__ == "__main__":
    sys.exit(main())
