"""Offline checks: must-keeps, render, no LLM."""

from __future__ import annotations

import json
from pathlib import Path

from resume_pipeline.fetch import resume_stem
from resume_pipeline.finalize import finalize, load_base, warnings_for
from resume_pipeline.render import _e, render

ROOT = Path(__file__).resolve().parents[1]


def _draft(base_name: str) -> dict:
    base = load_base(ROOT, base_name)
    bottom = base["projects"][-1]["id"]
    return {
        "company": "Example",
        "role": "Intern",
        "base": base_name,
        "target_team": "",
        "fit_summary": "Test.",
        "replaced_bottom_id": bottom,
        "keep_cut": [{"id": bottom, "action": "cut", "reason": "replaced"}],
        "coursework": base["coursework"],
        "skills": base["skills"],
        "work": [
            {
                "id": "amazon",
                "title": "Software Development Intern",
                "bullets": base["work"][0]["bullets"],
            }
        ],
        "projects": [
            {"id": p["id"], "name": p["name"], "role": p["role"], "bullets": p["bullets"]}
            for p in base["projects"]
            if p["id"] != bottom
        ],
        "new_project": {
            "name": "Tiny Runtime MVP",
            "role": "Independent Project",
            "location": "Remote",
            "dates": "Jan. 2026 -- Present",
            "what_it_is": "A small C++ kernel with PyTorch bindings.",
            "mvp": "One fused op, tests, Docker.",
            "stretch_off_resume": "JAX + Kubernetes",
            "bullets": [
                "Implemented a fused C++ kernel with Python bindings and checked numeric parity against eager PyTorch on CPU.",
                "Packaged the runtime in Docker and gated unit tests in GitHub Actions.",
            ],
        },
        "keyword_map": [{"keyword": "PyTorch", "where": "new_project"}],
    }


def test_amazon_four_and_bottom_replaced():
    for name, ml in (("swe", False), ("mle", True)):
        base = load_base(ROOT, name)
        out = finalize(base, _draft(name), ml_role=ml)
        assert out["work"][0]["id"] == "amazon"
        assert len(out["work"][0]["bullets"]) == 4
        ids = [p["id"] for p in out["projects"]]
        assert base["projects"][-1]["id"] not in ids
        if ml:
            assert "algoverse" in ids
        profile = json.loads((ROOT / "data" / "profile.json").read_text())
        tex = render(profile, out, (ROOT / "templates" / "resume.tex").read_text())
        assert "\\begin{document}" in tex
        assert "Tiny Runtime MVP" in tex
        assert "**" not in tex
        assert r"\textbf{78\%}" in tex
        assert r"\textbf{" in tex
        assert warnings_for(out) is not None


def test_skip_new_project_keeps_bottom():
    for name, ml in (("swe", False), ("mle", True)):
        base = load_base(ROOT, name)
        bottom = base["projects"][-1]["id"]
        draft = _draft(name)
        draft["add_new_project"] = False
        draft["replaced_bottom_id"] = bottom
        draft["new_project"] = {
            "name": "Should Not Appear",
            "bullets": ["x" * 90, "y" * 90],
        }
        out = finalize(base, draft, ml_role=ml)
        ids = [p["id"] for p in out["projects"]]
        assert bottom in ids
        assert out["new_project"] is None
        assert out["add_new_project"] is False
        profile = json.loads((ROOT / "data" / "profile.json").read_text())
        tex = render(profile, out, (ROOT / "templates" / "resume.tex").read_text())
        assert "Should Not Appear" not in tex
        assert base["projects"][-1]["name"] in tex


def test_sim_escape():
    assert r"$\sim$50\%" in _e("cutting wrong diagnoses by ~50%.")
    assert r"$<$1\%" in _e("from ~88% to <1%.")


def test_bold_render():
    assert r"\textbf{78\%}" in _e("accuracy to **78%**.")
    assert r"\textbf{$\sim$50\%}" in _e("by **~50%**.")
    assert r"\textbf{Kotlin}" in _e("using **Kotlin** on AWS.")
    assert "**" not in _e("using **Kotlin** on AWS.")


def test_apply_bold_from_base_pattern():
    from resume_pipeline.bold import apply_bold

    infosys = (
        "Reduced manual lookup time by 40% and cut query latency to under 3 seconds "
        "by building an agentic Retrieval Augmented Generation system that indexed "
        "10,000+ corporate documents using Pydantic AI."
    )
    marked = apply_bold(infosys)
    assert "**40%**" in marked
    assert "**under 3 seconds**" in marked
    assert "**Retrieval Augmented Generation**" in marked
    assert "**10,000+**" in marked
    assert "**Pydantic AI**" in marked
    assert apply_bold(marked) == marked

    pg = apply_bold("stored rows in PostgreSQL and ran SQL reports.")
    assert "**PostgreSQL**" in pg
    assert "**SQL**" in pg
    assert "Postgre**SQL**" not in pg


def test_unmatched_bold_raises():
    base = load_base(ROOT, "swe")
    draft = _draft("swe")
    draft["work"][0]["bullets"] = [
        "Wrote **277 tests without closing the mark.",
        base["work"][0]["bullets"][1],
        base["work"][0]["bullets"][2],
        base["work"][0]["bullets"][3],
    ]
    try:
        finalize(base, draft, ml_role=False)
        raise AssertionError("expected unmatched ** to fail")
    except ValueError as exc:
        assert "Unmatched" in str(exc)


def test_resume_stem():
    assert (
        resume_stem("Apple", "Machine Learning Intern", "jobs-apple-long-slug")
        == "apple-machine-learning-intern"
    )
    assert resume_stem("", "", "fallback-slug") == "fallback-slug"


if __name__ == "__main__":
    test_sim_escape()
    test_bold_render()
    test_apply_bold_from_base_pattern()
    test_amazon_four_and_bottom_replaced()
    test_unmatched_bold_raises()
    test_skip_new_project_keeps_bottom()
    test_resume_stem()
    print("ok")
