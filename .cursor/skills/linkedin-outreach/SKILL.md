---
name: linkedin-outreach
description: >-
  Drafts 300-character LinkedIn connection notes for Vibhas Nair after
  researching employees in a logged-in LinkedIn browser session. Run after
  every resume tailor / application, and whenever the user asks for outreach,
  LinkedIn notes, connection notes, recruiter messages, hiring-manager
  messages, or cold reach-out.
---

# LinkedIn outreach

Draft connection notes. Never click Connect or Send. Never invent people.

If this is not the `resume-pipeline` repo, `cd` there (or ask) before writing files.

Read `data/outreach_prefs.json`, `data/internship_prefs.json`, `data/profile.json`, and the JD (`work/<slug>/jd.md` if present). For gold/bad notes see [examples.md](examples.md).

## When to run

**Run** after every resume tailor / application, and whenever the user asks for outreach / LinkedIn / connection notes / recruiter or hiring-manager messages / cold reach-out.

If this chat also has a job URL (or a tailor was requested): finish the tailor-resume skill first, then continue here using that JD.

If there is no JD yet and they named a company/role: fetch or reuse `work/<slug>/jd.md` (`python tailor.py "<URL>"` is fine for fetch-only). Do not rewrite resume bullets unless they also asked to tailor.

Intern term: from the JD; Spring 2027 and Summer 2027 are both in-scope. If the JD is missing a term, use `intern_terms` in prefs.

## Workflow

1. Load prefs + profile + JD. Score north-star alignment (NVIDIA Cosmos, Tesla Optimus, RL, world models, robot foundation models, training/inference). Alignment changes **effort**, not template family: high interest → deeper research and maybe an HM note; low interest → still Type 1 ICs + recruiter. Never open with Type 2.
2. Find people in the Cursor browser (logged-in LinkedIn). Cap: **1 recruiter + 2–3 ICs + at most 1 hiring manager**. Open at most `max_profiles_opened` (5) profiles. Do not mass-scrape.
3. For each candidate: copy the **profile URL** from the browser (strip tracking query params; keep `https://www.linkedin.com/in/...`). For ICs, read current-role tenure (`Mar 2025 – Present · 1 yr 6 mos`). Keep only `ic_tenure_months.min`–`max` (6–24 months) at this company; skip under ~6 months or over ~2 years. Require a **profile-specific hook** from *their* Experience / About / Featured (named sub-team, system, project, tool) — not the JD team title. If About is generic, optionally search Scholar / GitHub / the company blog. Still no personal hook → skip. Do not invent specialties or `/in/` slugs.
4. Classify persona and draft a connection note (hard cap **300** characters, spaces and punctuation included).
5. Apply the critic checklist. Rewrite or drop failures.
6. Write **only** `resumes/<company>-<role>-outreach.md`. In the **chat reply**, paste every kept person's LinkedIn URL (name + persona + link). Point at the outreach file (and the resume tex/pdf if this run also tailored). Do not mention `work/` unless the run failed.

Type 2 (study A vs B) is **not** a connection note. Write a longer post-accept DM only if the user asks.

## Browser (LinkedIn)

Use the Cursor browser. Order: `browser_tabs` list → `browser_navigate` to LinkedIn if needed → `browser_lock` → search/open profiles → `browser_lock` unlock when **all** browser work for this run is done.

**Stop** on login wall, captcha, checkpoint, or logged-out home. Ask the user to log in or paste search results. Do not invent people.

Never click **Connect**, **Send**, **Follow**, or InMail send. Drafts only.

### Search recipe

1. People search, current company = the employer. Add team keywords from the JD (`target_team` if given).
2. Prefer the UNC-Chapel Hill school filter. If the UI has no school facet, add keyword `UNC` or `Chapel Hill` (`school_search` in prefs).
3. **ICs:** current company tenure **6 months–2 years** (`ic_tenure_months`). Prefer people on the posting’s team. Title can be SWE / SWE II / engineer; converted intern in that window still uses the IC template. Skip staff, principal, distinguished, VP, C-level. Skip current-role tenure under ~6 months (still ramping) or over ~2 years. Do not use intern / new grad / grad year as the default filter.
4. **Recruiter:** university / intern / technical recruiter for that company. One only.
5. **HM:** one manager / head / director on that team. Skip execs.

Rank: UNC + on the posting’s team + in the tenure window > other ICs in-window on the team > intern recruiter > HM. Skip people who left, “don’t DM for referrals,” or who are off-team. Do not message more than 3 ICs on the same small team.

If search yields nobody usable: write the outreach file with an empty kept list and say what blocked you (login, no UNC hits, tenure misses, generic titles only).

## Personas and templates

One ask. ICs: the brief-chat sentence in the template (no referral, no second CTA). Recruiters and HMs: connecting only. No resume URL. UNC is a ranking boost, not the only hook. Amazon is an intern credential, not senior tenure.

Pick **one** credential from prefs that maps to their work — **recruiters and HMs only**. Default: `amazon` / `amazon_hm`. ML/research teams may use `neurips`. RAG/agents JDs may use `infosys`. ICs do not pitch credentials.

**IC** (connection request; 6 months–2 years at this company). First barrier of entry: this template only. The unique noun must come from **their** current role, not the JD. `[relevant interest]` is north-star or JD-aligned (Cosmos, RL, autonomy infra). `[specific work they have done]` is one artifact from their bullets. If another IC on the same posting could swap in and the sentence stays true, rewrite or skip. Boilerplate is ~190 characters; keep slots tight. Shorten `[role]` (`Software Engineer` → `engineer`) if the note would exceed 300.

```
Hi {Name}, I'm Vibhas! I saw that you're a {role} at {company}, working on {specific work/team}. I'm interested in {relevant interest} and in {specific work they have done}, and would love to know more about your work at {company}. Would you be open to a brief chat about your experiences?
```

**Recruiter** (connection request). Role they are hiring for + one mapped past experience + interest in this posting + connect. `{relevant past experience}` is **one** credential from prefs (`amazon`, `neurips`, or `infosys`) that matches the JD. `{relevant job posting}` is the intern role/team, not a generic “your company.” No resume URL. Shorten slots if over 300.

```
Hi {Name}, I'm Vibhas! I saw that you're hiring for {role} at {company}. I've worked on {relevant past experience}, I'm interested in {relevant job posting}, and I think I would be a great fit for this position. Would love to connect!
```

**Hiring manager** (connection request). Same spine as recruiter, plus their work: `{their team/work}` and `{their work}` must be a noun from the HM’s Experience or the team problem they own — not only the JD title.

```
Hi {Name}, I'm Vibhas! I saw that you're hiring for {role} at {company}, working on {their team/work}. I've worked on {relevant past experience}, I'm interested in {their work}, and I think I would be a great fit for this position. Would love to connect!
```

If swapping the **name** still works (same team, same JD nouns), rewrite or skip. JD team name alone (“Software Infra,” “infra tooling”) is not a hook.

## Critic (before writing the file)

- [ ] `len(note) <= 300` (count every character). Hard-fail over 300.
- [ ] ICs: one ask is the brief-chat sentence. Recruiters/HMs: one ask is connecting. No referral, no study list, no second CTA.
- [ ] No URL, no resume attachment line **inside the note**.
- [ ] Every kept person has a real `linkedin.com/in/...` URL copied from the browser (not guessed from their name).
- [ ] Hook is a real proper noun from **their** Experience / About / Featured / a public artifact — not the JD team title.
- [ ] JD-only hook fails: “researching Software Infra” / “infra tooling there” and similar.
- [ ] IC tenure is 6–24 months at this company (skip if outside; recruiters/HMs exempt).
- [ ] UNC is not the only sentence.
- [ ] Amazon not framed as years of industry seniority.
- [ ] ICs use the IC template, not a recruiter pitch. Converted intern in the tenure window still uses IC.
- [ ] Recruiter notes name the intern role they are hiring for and one real past experience. HM notes also name **their** work, not only the JD.
- [ ] Not Type 2 as the opener.

## Output file

`resumes/<company>-<role>-outreach.md` — same slug as the resume. Copy-paste ready:

```markdown
# {Company} {Role} — LinkedIn connection notes

Intern term: {term}
North-star alignment: high | medium | low ({why})

## {Name} — {persona: ic | recruiter | hiring_manager}

- Profile: https://www.linkedin.com/in/{slug}/
- Tenure: {e.g. 1 yr 4 mos}
- Team: ...
- Hook: ...
- Why them: ...
- Keep: yes

Note ({N}/300):

{note}

```

Include skipped candidates in a short `## Skipped` list (name, profile URL if known, reason). No fabricated profiles.

## Chat reply (required)

After writing the file, the user-facing message **must** list each kept person with their profile link pasted in chat, not only in the markdown file:

```
Notes: resumes/<company>-<role>-outreach.md

- {Name} ({persona}): https://www.linkedin.com/in/{slug}/
- {Name} ({persona}): https://www.linkedin.com/in/{slug}/
```

Do not finish without those links. If LinkedIn blocked you before any profile opened, say so and list nobody.
