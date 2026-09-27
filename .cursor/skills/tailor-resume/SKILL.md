---
name: tailor-resume
description: >-
  Tailors a SWE/MLE internship resume from a job posting into
  resumes/<company>-<role>.tex and .pdf via this repo's pipeline. Use
  immediately when the user pastes a job or careers URL (Greenhouse, Ashby,
  Lever, Workday, LinkedIn, jobs.apple.com, company /jobs /careers /intern
  pages), pastes a job description, names a target team with a posting, or
  asks to tailor, customize, write, or generate a resume for a role,
  internship, or job posting. Do not wait for them to mention AGENTS.md.
---

# Tailor resume

You are the writer LLM. Do not call Anthropic, OpenAI, or any external completion API. Do not rewrite `templates/resume.tex`. `--llm` only if the user asks.

If this is not the `resume-pipeline` repo, `cd` there (or ask) before running.

Read `data/internship_prefs.json` and `data/targets.json`. Terms and the SWE/ML mix come from those files. URLs they paste are pre-vetted: always tailor; do not skip or warn that a posting is off-strategy. Use `"base": "mle"` or `"base": "swe"` according to `role_mix` and the posting. After a successful tailor, follow `.cursor/skills/linkedin-outreach/` and append the company/role to `data/targets.json` if it is new.

## Workflow

For each URL (or pasted JD). Optional `--team "..."` when they name a target team.

1. `python tailor.py "<URL>" --team "<if given>"`  
   Writes `work/<slug>/jd.md` only. Does not generate bullets.  
   If they pasted the JD instead of a URL, write `work/<slug>/jd.md` yourself, then continue.
2. Read `prompts/writer.md`, `prompts/examples.md`, `work/<slug>/jd.md`, `data/base_swe.json`, and `data/base_mle.json`. Write `work/<slug>/result.json` (JSON only, no fences).
3. Apply `prompts/critic.md`. Overwrite `result.json`.
4. `python tailor.py --from-json work/<slug>/result.json`  
   Writes **only** `resumes/<company>-<role>.tex` and `.pdf`.
5. Point the user at those two files. Do not mention `work/`, `REVIEW.md`, or `result.json` unless the run failed.
6. Then follow `.cursor/skills/linkedin-outreach/` (outreach file plus each person's profile URL in chat). Append the company/role to `data/targets.json` if it is new.

Batch: run the same four steps per URL. Do not skip the critic pass.

## Rules

- Honor `must_keep` and `bullet_count` on work entries in the base JSON.
- On ML jobs, keep projects with `must_keep_ml`.
- New last project (2–3 bullets, ~80 hours, replaces only the bottom project) **only** when the JD needs tech the current page lacks. Otherwise keep every existing project.
- Voice: `prompts/examples.md`, plus XYZ / compressed STAR.
- Bold metrics and key tech with `**span**` like the base resumes. Never `\textbf{}` in JSON.
- Existing metrics and entry **dates** must not change (copy from the base JSON). Do not rewrite a finished date range to `Present`. New-project metrics are conservative estimates (never `[placeholder]`).
- No professional summary. Target team overrides a generic JD when they conflict.
- Coursework: start from the base line. Add classes from `data/internship_prefs.json` `extra_coursework` when the JD matches `use_when`. Keep ~3–4 classes.

## Routing

Read `role_mix` in `data/internship_prefs.json`.

- ML / research / MLE / AI / ML systems internships → `"base": "mle"`
- SDE / backend / product internships with little ML → `"base": "swe"`
- If ambiguous, use the mix the prefs treat as the default
