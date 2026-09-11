# Job prep

A Cursor + Python workflow for internship applications. Paste a job URL; the agent tailors a one-page resume to that posting, then drafts LinkedIn connection notes for people on the team.

Python fetches the job description and fills a locked LaTeX template. The Cursor agent writes the bullets and the outreach notes. You do not need an Anthropic or OpenAI key unless you opt into `--llm`.

Personal profile data, generated resumes, and job-scratch files stay local (see [What is not in git](#what-is-not-in-git)).

## What it does

1. **Resume tailor** (`.cursor/skills/tailor-resume/`) — On a job or careers URL, fetch the JD, rewrite experience against two base resumes (SWE vs ML), and write `resumes/<company>-<role>.tex` and `.pdf`.
2. **LinkedIn outreach** (`.cursor/skills/linkedin-outreach/`) — After a tailor (or when you ask), find people on that team in a logged-in LinkedIn browser session and draft 300-character connection notes. It never clicks Connect or Send.

Agent playbook: `AGENTS.md`. Writer/critic prompts: `prompts/`.

## Requirements

- **[Cursor](https://cursor.com)** with Agent mode (the skills under `.cursor/skills/` run here)
- **Python 3.10+**
- **[latexmk](https://mg.readthedocs.io/latexmk.html)** (MacTeX or TeX Live) if you want PDFs; use `--no-pdf` for LaTeX only
- Packages in `requirements.txt` (`httpx`, `python-dotenv`)
- **LinkedIn in the Cursor browser**, logged in, only if you want outreach notes
- Optional: `ANTHROPIC_API_KEY` or `OPENAI_API_KEY` in `.env` for `python tailor.py URL --llm` (skips the Cursor writer)

Your own `data/*.json` files are required for a real run. They are gitignored so clones do not receive someone else’s profile, resume bullets, or application list. Copy the shapes below (or keep your own files if you already have them).

| File | Role |
|---|---|
| `data/profile.json` | Name, school, contact, LinkedIn |
| `data/base_swe.json` / `data/base_mle.json` | Two base resumes the tailor rewrites from |
| `data/internship_prefs.json` | Terms, location, authorization, search priorities |
| `data/outreach_prefs.json` | Connection-note identity, north-star topics, credential one-liners |
| `data/targets.json` | Living list of companies/roles already tailored |

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Open this folder in Cursor. Put your JSON under `data/` (the directory is ignored; create it locally). Copy `.env.example` to `.env` only if you use `--llm`.

## Usage

**Cursor.** Agent mode. A job URL is enough; you can add a team:

```
https://...
Target team: <optional, e.g. ML runtimes>
```

The agent will:

1. `python tailor.py "<URL>" --team "..."` — fetch the JD into `work/<slug>/`
2. Write bullets with `prompts/writer.md` and `prompts/critic.md`
3. `python tailor.py --from-json work/<slug>/result.json` — `resumes/<company>-<role>.tex` + `.pdf`
4. Draft LinkedIn notes in `resumes/<company>-<role>-outreach.md` and paste profile URLs in chat

**CLI** (fetch and render only; the agent still writes `result.json` unless you pass `--llm`):

```bash
python tailor.py "https://..." --team "ML runtimes"
python tailor.py --from-json work/<slug>/result.json
```

## Output

`resumes/` (gitignored except `.gitkeep`):

- `<company>-<role>.tex`
- `<company>-<role>.pdf`
- `<company>-<role>-outreach.md`

`work/<slug>/` (gitignored): `jd.md`, `result.json`

## What is not in git

| Path | Why |
|---|---|
| `data/*.json` | Personal profile, resume bases, prefs, targets |
| `resumes/*` | Tailored applications |
| `work/` | Per-job scratch |
| `.env` | API keys |

## Layout

```
data/            local JSON (gitignored) — profile, bases, prefs, targets
prompts/         writer, critic, few-shots for the Cursor agent
templates/       locked LaTeX resume
resume_pipeline/ fetch, finalize, render
tailor.py        prepare + render
resumes/         tex + pdf + outreach.md (gitignored)
work/            per-job scratch (gitignored)
AGENTS.md        agent playbook
.cursor/skills/tailor-resume/       job URL / tailor resume
.cursor/skills/linkedin-outreach/   connection notes after each tailor
```
