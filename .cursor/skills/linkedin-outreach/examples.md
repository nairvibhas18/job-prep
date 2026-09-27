# Connection note examples

Count every character (spaces, punctuation, newlines). Cap is 300. These notes are single paragraph, no trailing newline in the count. Names, schools, and employers here are fictional. `{first_name}` and credential lines come from `data/outreach_prefs.json`.

## Gold — IC (connection request; tenure 6 months–2 years)

**Chars: 289**

```
Hi Alex, I'm Jordan! I saw that you're an engineer at Northwind, working on the payments API. I'm interested in distributed systems and in your idempotency work on checkout, and would love to know more about your work at Northwind. Would you be open to a brief chat about your experiences?
```

Hook is from **their** Experience (payments API, idempotency on checkout), not the JD team name. Converted intern in the 6–24 month window uses this same shape. Shorten `{role}` if the note would exceed 300.

Dossier lines (not in the 300-char note): `- Profile: https://www.linkedin.com/in/example-alex/` and `- Tenure: 1 yr 4 mos`

Chat must paste that URL next to their name.

## Gold — Recruiter

**Chars: 259**

```
Hi Sam, I'm Jordan! I saw that you're hiring for a backend intern at Northwind. I've worked on API reliability for a payments service, I'm interested in the intern role on that team, and I think I would be a great fit for this position. Would love to connect!
```

Role they are hiring for + one mapped experience from prefs + this posting. No resume URL.

## Gold — Hiring manager

**Chars: 262**

```
Hi Riley, I'm Jordan! I saw that you're hiring for an ML intern at Northwind, working on ranking. I've worked on model evaluation for search, I'm interested in your ranking experiments, and I think I would be a great fit for this position. Would love to connect!
```

Recruiter spine plus **their** work (ranking experiments). Not a school-only note.

## Bad (do not write)

**JD-only hook** — fails the swap test:

```
Hey Alex — Jordan, Example University CS (May '28). Came across your profile while researching Payments at Northwind. Would love to learn how you're approaching infra tooling there if you're open to connecting.
```

Any other Payments IC could replace Alex. Use a noun from *their* bullets (sub-team, a named system) or skip.

**Tenure** — IC started 2 months ago, or 5 years on the team. Keep 6 months–2 years at this company.

**Too long** — a full DM. Connection notes must truncate; put the long version only in a post-accept DM if asked.

**Referral ask** — “Would you be open to referring me?” ICs ask for a brief chat; recruiters/HMs ask to connect. Never a referral.

**School-only** — “Hey Sam, fellow classmate — would love to connect.” Swap the name and it still works; skip or rewrite with a work hook.

**Type 2 opener** — “What should I study for the intern loop?” Homework ask. Not a connection note.

**Resume link** — “Here’s my resume: linkedin.com/in/example.” Profile is enough; no URL in the note.

**Recruiter pitch to an IC** — highlight-reel credentials at an engineer. ICs get the profile-specific template.

**Invented profile URL** — do not guess `linkedin.com/in/firstname-lastname`. Copy the URL from the open profile tab.

**Inflated seniority** — “I’ve had over 5 years of technical experience” when the credential in prefs is an internship.
