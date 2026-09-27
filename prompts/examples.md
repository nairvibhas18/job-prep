# Voice few-shots (shape only)

These bullets are fictional. They show cadence, not a real resume. Match this shape: concrete verb, specific tech, real problem, one number. Plain English. Do not sound like a keyword cloud or a systems-design doc.

When a base entry has `"voice_example": true`, match that entry's density instead of copying these sentences onto someone else's jobs.

## Research voice

- Trained a small classifier in **PyTorch** and lifted held-out accuracy by **6 points** over the previous baseline.
- Wrote an evaluation script that reran the same **500** examples after each change so regressions were visible before the write-up.

## Product / systems voice

- Shipped a **FastAPI** endpoint that cut failed checkouts by **18%** by retrying idempotent payment calls.
- Built the signup flow in **React** (**Next.js**) with one other engineer, from the schema through the production deploy.
- Automated production deploys with **GitHub Actions** and tightened the slowest **SQL** query on the account page.

## Bolding (JSON `**span**` → LaTeX `\textbf`)

In `result.json` mark spans with `**double asterisks**`. Never write `\textbf{}` and never leave `**` in the PDF (the renderer converts them).

Bold:

- Metrics and counts: **18%**, **6 points**, **500**
- Key technologies and named methods in that bullet: **FastAPI**, **PyTorch**, **React** (**Next.js**), **SQL**

Do not bold whole clauses, verbs, or company names (headings are already bold). Typical bullet: 3–6 spans. A bullet may have none. When you keep a base bullet, keep its `**` marks. When you rewrite, re-mark the same classes of spans. New-project bullets follow the same pattern.

## Shape (XYZ / STAR) — structure only, not voice

Use the **XYZ formula**: accomplished **[X]** as measured by **[Y]**, by doing **[Z]**.

That is the resume form of **STAR** (Situation/Task compressed into the problem, Action = Z, Result = Y). Start with a strong action verb. Put tech in Z. Put numbers in Y. Do not write a four-sentence STAR story.

Same idea as: [Action verb] + [technical implementation] + [specific problem] + [measured impact]

Bad: "Built a chatbot using Python"

Good: "Engineered a FastAPI service using **retrieval over internal docs**, cutting lookup time by **40%** on a **10,000+** document set"

Shape references (do **not** copy these facts onto jobs that did not do this work):

- Led the signup form in React and TypeScript, raising completion by 12% and cutting load time on that page.
- Fine-tuned a small text model in PyTorch, improving task accuracy by 8 points on a held-out set of 500 examples.

Prefer **one or two metrics**, not a list. If two metrics, they must both be true (existing jobs: only metrics already on the base resume).

## Banned phrasing

leverage, utilize, cutting-edge, robust, synergistic, ground-breaking, passionate, excited to, proven track record, results-driven, "played a key role"
