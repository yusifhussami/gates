import subprocess
import sys
from pathlib import Path

from run_evals import filter_by_tags
from gates.case import Case

ROOT = Path(__file__).resolve().parents[1]


def test_filter_by_tags_keeps_matching_only():
    a = Case(id="a", input="x", expect="y", scorer=lambda g, e: g == e, tags=("travel",))
    b = Case(id="b", input="x", expect="y", scorer=lambda g, e: g == e, tags=("billing",))
    kept = filter_by_tags([a, b], "travel")
    assert [c.id for c in kept] == ["a"]


def test_filter_by_tags_no_match_returns_empty():
    a = Case(id="a", input="x", expect="y", scorer=lambda g, e: g == e, tags=("travel",))
    assert filter_by_tags([a], "nope") == []


def test_cli_tags_filter_runs_subset():
    proc = subprocess.run(
        [
            sys.executable,
            str(ROOT / "run_evals.py"),
            str(ROOT / "evals" / "intent_routing.yaml"),
            "--fn",
            "examples.demo_router:route",
            "--tags",
            "travel",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "1/1 passed" in proc.stdout
    assert "book_flight" in proc.stdout


def test_cli_tags_no_match_is_clear_error():
    proc = subprocess.run(
        [
            sys.executable,
            str(ROOT / "run_evals.py"),
            str(ROOT / "evals" / "intent_routing.yaml"),
            "--fn",
            "examples.demo_router:route",
            "--tags",
            "nope",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 2
    assert "no cases match --tags" in proc.stderr


def test_cli_missing_suite_file_is_clear_error():
    proc = subprocess.run(
        [
            sys.executable,
            str(ROOT / "run_evals.py"),
            str(ROOT / "evals" / "nope.yaml"),
            "--fn",
            "examples.demo_router:route",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 2
    assert "can't find suite file" in proc.stderr
