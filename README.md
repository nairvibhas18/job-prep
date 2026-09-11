# Job prep

Cursor skills plus a small Python pipeline for internship applications: tailor a one-page resume from a job URL, then draft LinkedIn connection notes for people on that team.

Paste a job URL (or “tailor this resume”) in the **Cursor Agents window**. The project skill `.cursor/skills/tailor-resume/` is meant to auto-trigger; you do not need to mention AGENTS.md. The agent writes bullets; Python fetches the posting and fills a locked LaTeX template.

The only files meant for you are in **`resumes/`** (`*.tex` and `*.pdf`, plus `*-outreach.md` after each tailor). Scratch (`work/`) is for the agent.

## From the Cursor Agents window

Open this folder. Agent mode. A URL is enough:

```
https://...
Target team: <optional, e.g. ML runtimes>
```

The agent will:

1. `python tailor.py "<URL>" --team "..."` — fetch JD into `work/<slug>/`  
2. Write `work/<slug>/result.json` using `prompts/writer.md` + `prompts/critic.md`  
3. `python tailor.py --from-json work/<slug>/result.json` — `resumes/<company>-<role>.tex` + `.pdf`
4. LinkedIn notes in `resumes/<company>-<role>-outreach.md`

No Anthropic/OpenAI key is required.

## LinkedIn notes

After every tailor, the agent drafts connection notes (you can also ask explicitly). It uses a logged-in LinkedIn tab in the Cursor browser to find people, then writes `resumes/<company>-<role>-outreach.md` (300-character connection notes) and pastes each person's LinkedIn profile URL in chat. It never clicks Connect or Send. If LinkedIn shows a login wall, log in (or paste search results) and continue.

Skill: `.cursor/skills/linkedin-outreach/`. Prefs: `data/outreach_prefs.json`, `data/internship_prefs.json`. Living targets: `data/targets.json`. Outreach runs after every tailor.

## CLI (same split)

```bash
cd ~/Projects/resume-pipeline
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python tailor.py "https://..." --team "ML runtimes"
# then the Cursor agent writes work/<slug>/result.json
python tailor.py --from-json work/<slug>/result.json
```

PDF compile needs `latexmk` (MacTeX / TeX Live). Use `--no-pdf` for LaTeX only.

Optional: `python tailor.py URL --llm` uses `ANTHROPIC_API_KEY` or `OPENAI_API_KEY` instead of the Cursor agent.

## What is enforced

| Rule | How |
|---|---|
| Amazon = 4 bullets | `finalize.py` |
| NeurIPS kept on ML jobs | `algoverse` must-keep when `base=mle` |
| New project last, 2–3 bullets, ~80h | only if the JD needs missing tech; else skip |
| Replaces only the bottom project | `tennis` (SWE) or `personalization` (MLE) when a new project is added |
| Voice | NeurIPS + Beautiful Together few-shots in `prompts/examples.md` |
| Strong bullets (XYZ / STAR) | Cursor agent writer + critic |
| Keywords | naturally in bullets/skills/project |
| No new tech on old jobs | writer `allowed_tech`; no Trainium/Neuron/etc. on the page |
| Existing metrics frozen | writer prompt |
| Conservative estimates | new project only |
| No summary / no leftover `**` / no `\\cite` | JSON `**span**` → `\\textbf`; renderer + checks |

## Output

`resumes/` — the deliverable:

- `<company>-<role>.tex`
- `<company>-<role>.pdf`
- `<company>-<role>-outreach.md` — after each tailor

`work/<slug>/` — scratch (gitignored): `jd.md`, `result.json`

## Layout

```
data/            profile, SWE/MLE bases, internship prefs, living targets, outreach prefs
prompts/         writer, critic, few-shots (for the Cursor agent)
templates/       locked LaTeX
resume_pipeline/ fetch, finalize, render
tailor.py        prepare + render
resumes/         tex + pdf + outreach.md
work/            per-job scratch
AGENTS.md        agent playbook
.cursor/skills/tailor-resume/       auto-trigger skill (job URL / tailor resume)
.cursor/skills/linkedin-outreach/   after every tailor (LinkedIn / connection notes)
```
