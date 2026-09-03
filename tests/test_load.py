from pathlib import Path

from gates.load import load_cases


def test_load_intent_suite():
    path = Path(__file__).resolve().parents[1] / "evals" / "intent_routing.yaml"
    cases = load_cases(path)
    assert len(cases) == 5
    assert cases[0].id == "greet"


def test_load_missing_field_gives_clear_error(tmp_path):
    bad = tmp_path / "bad.yaml"
    bad.write_text("- id: oops\n  input: hi\n")  # no expect
    try:
        load_cases(bad)
        assert False, "expected ValueError"
    except ValueError as exc:
        msg = str(exc)
        assert "missing required field 'expect'" in msg
        assert "oops" in msg


def test_load_unknown_scorer_gives_clear_error(tmp_path):
    bad = tmp_path / "bad.yaml"
    bad.write_text("- id: oops\n  input: hi\n  expect: yes\n  scorer: nope\n")
    try:
        load_cases(bad)
        assert False, "expected ValueError"
    except ValueError as exc:
        assert "unknown scorer 'nope'" in str(exc)


def test_load_string_tags_gives_clear_error(tmp_path):
    bad = tmp_path / "bad.yaml"
    bad.write_text("- id: oops\n  input: hi\n  expect: yes\n  tags: baseline\n")
    try:
        load_cases(bad)
        assert False, "expected ValueError"
    except ValueError as exc:
        assert "'tags' should be a list" in str(exc)
