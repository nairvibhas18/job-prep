"""Merge LLM output with base resumes and enforce must-keeps."""

from __future__ import annotations

from copy import deepcopy

from resume_pipeline.bold import apply_bold, strip_bold


BANNED_EMPLOYER_STACK = (
    "trainium",
    "inferentia",
    "graviton",
    "neuron sdk",
    "neuron-sdk",
    "prime-rl",
    "verifiers",
    "nitro system",
)

WEAK_OPENERS = (
    "worked on",
    "helped with",
    "responsible for",
    "was tasked",
)


def load_base(root, name: str) -> dict:
    import json
    from pathlib import Path

    path = Path(root) / "data" / f"base_{name}.json"
    return json.loads(path.read_text(encoding="utf-8"))


def finalize(base: dict, draft: dict, *, ml_role: bool) -> dict:
    """Apply must-keeps after the model writes. Mutates a copy of draft."""
    out = deepcopy(draft)
    out["base"] = base["base"] if out.get("base") not in ("swe", "mle") else out["base"]

    cuts = {k["id"] for k in out.get("keep_cut") or [] if k.get("action") == "cut"}
    work_out = []
    for entry in base["work"]:
        if entry["id"] in cuts and not entry.get("must_keep"):
            continue
        drafted = _by_id(out.get("work") or [], entry["id"]) or {}
        bullets = list(drafted.get("bullets") or entry["bullets"])
        need = entry.get("bullet_count")
        if isinstance(need, int) and need > 0 and len(bullets) != need:
            padded = (bullets + list(entry["bullets"]))[:need]
            bullets = padded if len(padded) >= need else list(entry["bullets"])
        work_out.append(
            {
                "id": entry["id"],
                "company": entry["company"],
                "title": drafted.get("title") or entry["title"],
                "location": entry["location"],
                "dates": entry["dates"],
                "bullets": _bold_bullets(bullets),
            }
        )
    out["work"] = work_out

    wants_new = _wants_new_project(out)
    out["add_new_project"] = wants_new
    if not wants_new:
        cuts -= _replace_cuts(out, _default_bottom(base))

    replaced = ""
    if wants_new:
        requested = out.get("replaced_bottom_id") or ""
        draft_ids = {p.get("id") for p in (out.get("projects") or [])}
        base_ids = {e["id"] for e in base["projects"]}
        if requested in base_ids:
            replaced = requested
        elif _default_bottom(base) not in draft_ids:
            replaced = _default_bottom(base)
        must_keep_projects = _must_keep_projects(base, ml_role)
        if replaced in must_keep_projects:
            replaced = _replaceable_bottom(base, must_keep_projects)
    out["replaced_bottom_id"] = replaced

    projects_out = []
    draft_projects = out.get("projects") or []
    base_by_id = {e["id"]: e for e in base["projects"]}
    ordered = []
    seen: set[str] = set()
    for drafted in draft_projects:
        eid = drafted.get("id")
        if eid in base_by_id and eid not in seen:
            seen.add(eid)
            ordered.append(base_by_id[eid])
    for entry in base["projects"]:
        if entry["id"] not in seen:
            seen.add(entry["id"])
            ordered.append(entry)
    for entry in ordered:
        if (replaced and entry["id"] == replaced) or entry["id"] in cuts:
            continue
        drafted = _by_id(draft_projects, entry["id"])
        if ml_role and entry.get("must_keep_ml"):
            projects_out.append(_project(entry, drafted or entry))
            continue
        projects_out.append(_project(entry, drafted or entry))
    out["projects"] = projects_out

    if wants_new:
        np = out.get("new_project") or {}
        bullets = np.get("bullets") or []
        if len(bullets) > 3:
            bullets = bullets[:3]
        if len(bullets) < 2:
            raise ValueError("new_project must have 2 or 3 bullets.")
        np["bullets"] = _bold_bullets(bullets)
        np.setdefault("role", "Independent Project")
        np.setdefault("location", "Remote")
        np.setdefault("dates", "Jan. 2026 -- Present")
        out["new_project"] = np
    else:
        out["new_project"] = None

    if not out.get("skills"):
        out["skills"] = base["skills"]
    if not out.get("coursework"):
        out["coursework"] = base["coursework"]

    _assert_banned(out)
    _assert_formula(out)
    return out


def warnings_for(out: dict) -> list[str]:
    notes = []
    for section, entries in (("work", out["work"]), ("projects", out["projects"])):
        for entry in entries:
            for i, bullet in enumerate(entry["bullets"], 1):
                low = bullet.lower()
                if any(w in low for w in WEAK_OPENERS):
                    notes.append(f"{entry['id']} bullet {i} uses a weak opener.")
                if len(strip_bold(bullet)) < 80:
                    notes.append(f"{entry['id']} bullet {i} looks short ({len(strip_bold(bullet))} chars).")
    np = out.get("new_project")
    if np:
        for i, bullet in enumerate(np["bullets"], 1):
            if any(w in bullet.lower() for w in WEAK_OPENERS):
                notes.append(f"new_project bullet {i} uses a weak opener.")
            if "[" in bullet and "]" in bullet:
                notes.append(f"new_project bullet {i} still has a [placeholder]; use a conservative estimate.")
    return notes


def _default_bottom(base: dict) -> str:
    return base["projects"][-1]["id"]


def _must_keep_projects(base: dict, ml_role: bool) -> set[str]:
    kept = set()
    for entry in base.get("projects") or []:
        if entry.get("must_keep") or (ml_role and entry.get("must_keep_ml")):
            kept.add(entry["id"])
    return kept


def _replaceable_bottom(base: dict, must_keep: set[str]) -> str:
    for entry in reversed(base.get("projects") or []):
        if entry["id"] not in must_keep:
            return entry["id"]
    return ""


def _by_id(entries: list, eid: str) -> dict | None:
    for entry in entries:
        if entry.get("id") == eid:
            return entry
    return None


def _project(base_entry: dict, drafted: dict) -> dict:
    return {
        "id": base_entry["id"],
        "name": drafted.get("name") or base_entry["name"],
        "role": drafted.get("role") or base_entry["role"],
        "location": base_entry["location"],
        "dates": base_entry["dates"],
        "bullets": _bold_bullets(drafted.get("bullets") or base_entry["bullets"]),
    }


def _assert_banned(out: dict) -> None:
    chunks = []
    for entry in out["work"] + out["projects"]:
        chunks.extend(entry["bullets"])
        chunks.append(entry.get("name", ""))
    np = out.get("new_project")
    if np:
        chunks.extend(np["bullets"])
        chunks.append(np.get("name", ""))
    for line in out.get("skills", {}).values():
        chunks.append(str(line))
    blob = " ".join(chunks).lower()
    for token in BANNED_EMPLOYER_STACK:
        if token in blob:
            raise ValueError(
                f"Banned employer-stack term {token!r} appeared on the resume. "
                "Do not name Trainium/Neuron/verifiers/etc. unless they are on the base resume."
            )


def _assert_formula(out: dict) -> None:
    all_bullets = []
    for entry in out["work"] + out["projects"]:
        all_bullets.extend(entry["bullets"])
    np = out.get("new_project")
    if np:
        all_bullets.extend(np["bullets"])
    for bullet in all_bullets:
        if bullet.count("**") % 2:
            raise ValueError("Unmatched ** in a bullet. Close every **span**.")
        if "\\textbf" in bullet:
            raise ValueError("Use **span** in JSON bullets, not \\textbf.")
        if "\\cite" in bullet:
            raise ValueError("Do not use \\cite.")


def _bold_bullets(bullets: list[str], extra=None) -> list[str]:
    return [apply_bold(b, extra) for b in bullets]


def _wants_new_project(draft: dict) -> bool:
    flag = draft.get("add_new_project")
    np = draft.get("new_project")
    has_bullets = isinstance(np, dict) and len(np.get("bullets") or []) >= 2
    if flag is False:
        return False
    if flag is True:
        return True
    return has_bullets


def _replace_cuts(draft: dict, bottom_id: str) -> set[str]:
    """Cuts that only exist to make room for a new project — undo them on skip."""
    drop = set()
    for item in draft.get("keep_cut") or []:
        if item.get("action") != "cut":
            continue
        reason = (item.get("reason") or "").lower()
        if item.get("id") == bottom_id or "replac" in reason or "new project" in reason:
            drop.add(item["id"])
    return drop


