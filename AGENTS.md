# Resume pipeline

You are the **writer LLM**. Do not call Anthropic, OpenAI, or any external completion API. Python only fetches the JD and fills LaTeX.

Read `data/internship_prefs.json` and `data/targets.json` before searching or tailoring. Spring 2027 and Summer 2027 are both in-scope. Prefer `"base": "mle"` when the posting is ML/research/systems; keep ~20% on `"base": "swe"`. Always tailor URLs they paste (they are pre-vetted). After each tailor, follow `.cursor/skills/linkedin-outreach/` and append the company/role to `data/targets.json` if it is new. Do not maintain a do-not-apply list.

When the user pastes a job URL (and optional target team):

1. `python tailor.py "<URL>" --team "<if given>"`  
   This writes `work/<slug>/jd.md` only. It does not generate bullets.
2. Read `prompts/writer.md` and `prompts/examples.md`. Read `work/<slug>/jd.md` plus `data/base_swe.json` and `data/base_mle.json`. Write `work/<slug>/result.json` (JSON only, no fences).
3. Apply `prompts/critic.md` to those bullets. Overwrite `result.json`.
4. `python tailor.py --from-json work/<slug>/result.json`  
   Finalize must-keeps and write **only** `resumes/<company>-<role>.tex` and `.pdf`.
5. Do not rewrite `templates/resume.tex` preamble or macros.
6. Amazon is always 4 bullets. NeurIPS / `algoverse` stays on ML jobs.
7. Add a new last project (2–3 bullets, ~80 hours, replaces only the bottom project) **only** when the JD needs tech the current page lacks. Otherwise keep every existing project.
8. Voice: NeurIPS + Beautiful Together. Bullets use XYZ / compressed STAR. Bold metrics and key tech with `**span**` like the base resumes.
9. Existing metrics must not change. New-project metrics are conservative estimates (never `[placeholder]`).
10. Point the user at `resumes/<company>-<role>.tex` and `.pdf`. Do not mention `work/`, `REVIEW.md`, or `result.json` unless the run failed.
11. After every tailor, follow `.cursor/skills/linkedin-outreach/`, point at `resumes/<company>-<role>-outreach.md`, and paste each person's LinkedIn profile URL in chat.

`--llm` is opt-in only (external API keys). Do not use it unless the user asks.
