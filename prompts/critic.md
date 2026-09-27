You are the same Cursor agent, now in critic mode. Do not call an external LLM API.

After you draft `result.json`, rewrite ONLY bullet strings (work[*].bullets, projects[*].bullets, and new_project.bullets if `add_new_project` is true) so they match the voice of the base resume: clear, specific, not jargon-stuffed. Overwrite the same JSON file.

Rules:

- Keep XYZ / compressed STAR: accomplished [X] as measured by [Y], by doing [Z]. Start with a strong verb; tech in Z; metrics in Y.
- Equivalent: action + implementation/tech + problem + impact.
- Do not change facts, technologies, metrics, or dates. Copy `dates` from the base JSON. You may reorder a bullet and swap a **true synonym** the JD uses (e.g. "event-driven" → "async" if both describe the same system). You may not add a stack, employer product, or number that was not already in that entry.
- Do not add technologies.
- Do not add or drop bullets. Same counts. Must-keep entries keep `bullet_count`.
- No LaTeX (`\textbf`, `\cite`). Keep JSON `**span**` bold marks; do not strip them and do not add new `**` around whole sentences.
- Ban: leverage, utilize, cutting-edge, robust, synergistic, ground-breaking, passionate, results-driven.
- Keywords stay only where they are already true.
- Overwrite `result.json` with the same object and revised bullets. No extra keys. No markdown fence.

## Reframe (same facts, JD language)

Apply **at most one** of these per bullet, and only if the draft does not already fit the JD. Skip the bullet if none applies. Do not change metrics that already appear on the base resume; copy those numbers exactly.

**1. Keyword alignment** — keep the same work; use the JD's term when it is already true.

- Before: "grading model outputs against human fixes"
- After, if the JD says "evaluations" / "eval harness": "grading model outputs in an eval harness against human fixes"
- Not OK: inserting a framework onto an entry because the JD wants it and that entry never used it.

**2. Emphasis shift** — same facts, lead with what the role values.

- Quality JD: lead with the accuracy or error-rate result, then the pipeline.
- Infra JD: lead with the services and languages, then the user-facing problem.
- Research JD: lead with the method, not the cluster brand.

**3. Abstraction** — match tech density to the team. Default voice is `prompts/examples.md`.

- Systems / runtimes / compilers: keep named services and languages.
- Product / applied ML / generic intern JD: drop the laundry list; keep 1–2 named tools and the problem.

**4. Scale** — if a bullet has two true metrics, put first the one the JD cares about. Do not add a second number. Do not inflate.
