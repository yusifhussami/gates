from pathlib import Path

from gates.load import load_cases


def test_load_intent_suite():
    path = Path(__file__).resolve().parents[1] / "evals" / "intent_routing.yaml"
    cases = load_cases(path)
    assert len(cases) == 6
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


def test_load_bad_scorer_gives_clear_error(tmp_path):
    bad = tmp_path / "bad.yaml"
    bad.write_text("- id: oops\n  input: hi\n  expect: smalltalk\n  scorer: nope\n")
    try:
        load_cases(bad)
        assert False, "expected ValueError"
    except ValueError as exc:
        assert "unknown scorer" in str(exc)


def test_load_duplicate_id_gives_clear_error(tmp_path):
    bad = tmp_path / "bad.yaml"
    bad.write_text(
        "- id: dup\n  input: hi\n  expect: smalltalk\n"
        "- id: dup\n  input: bye\n  expect: smalltalk\n"
    )
    try:
        load_cases(bad)
        assert False, "expected ValueError"
    except ValueError as exc:
        assert "duplicate id" in str(exc)


def test_load_bad_tags_gives_clear_error(tmp_path):
    bad = tmp_path / "bad.yaml"
    bad.write_text("- id: oops\n  input: hi\n  expect: smalltalk\n  tags: travel\n")
    try:
        load_cases(bad)
        assert False, "expected ValueError"
    except ValueError as exc:
        assert "'tags' should be a list" in str(exc)


def test_load_null_tags_treated_as_no_tags(tmp_path):
    p = tmp_path / "cases.yaml"
    p.write_text("- id: ok\n  input: hi\n  expect: smalltalk\n  tags:\n")
    cases = load_cases(p)
    assert cases[0].tags == ()


def test_load_unhashable_id_gives_clear_error(tmp_path):
    bad = tmp_path / "bad.yaml"
    bad.write_text("- id: [oops]\n  input: hi\n  expect: smalltalk\n")
    try:
        load_cases(bad)
        assert False, "expected ValueError"
    except ValueError as exc:
        assert "'id' should be a plain value" in str(exc)


def test_load_empty_id_still_shown_in_error(tmp_path):
    bad = tmp_path / "bad.yaml"
    bad.write_text("- id: ''\n  input: hi\n  expect: smalltalk\n  scorer: nope\n")
    try:
        load_cases(bad)
        assert False, "expected ValueError"
    except ValueError as exc:
        assert "('')" in str(exc)


def test_load_non_string_id_gives_clear_error(tmp_path):
    bad = tmp_path / "bad.yaml"
    bad.write_text("- id: 123\n  input: hi\n  expect: smalltalk\n")
    try:
        load_cases(bad)
        assert False, "expected ValueError"
    except ValueError as exc:
        assert "'id' should be a string" in str(exc)


def test_load_non_string_note_gives_clear_error(tmp_path):
    bad = tmp_path / "bad.yaml"
    bad.write_text("- id: oops\n  input: hi\n  expect: smalltalk\n  note: [known, flaky]\n")
    try:
        load_cases(bad)
        assert False, "expected ValueError"
    except ValueError as exc:
        assert "'note' should be a string" in str(exc)


def test_load_non_string_tag_gives_clear_error(tmp_path):
    bad = tmp_path / "bad.yaml"
    bad.write_text("- id: oops\n  input: hi\n  expect: smalltalk\n  tags: [1]\n")
    try:
        load_cases(bad)
        assert False, "expected ValueError"
    except ValueError as exc:
        assert "each tag should be a string" in str(exc)


def test_load_non_string_input_gives_clear_error(tmp_path):
    bad = tmp_path / "bad.yaml"
    bad.write_text("- id: oops\n  input: 123\n  expect: smalltalk\n")
    try:
        load_cases(bad)
        assert False, "expected ValueError"
    except ValueError as exc:
        assert "'input' should be a string" in str(exc)


def test_load_cases_importable_from_gates_top_level():
    import gates

    assert gates.load_cases is load_cases


def test_load_unhashable_scorer_gives_clear_error(tmp_path):
    bad = tmp_path / "bad.yaml"
    bad.write_text("- id: oops\n  input: hi\n  expect: smalltalk\n  scorer: [nope]\n")
    try:
        load_cases(bad)
        assert False, "expected ValueError"
    except ValueError as exc:
        assert "'scorer' should be a plain value" in str(exc)


def test_load_non_list_yaml_gives_clear_error(tmp_path):
    bad = tmp_path / "bad.yaml"
    bad.write_text("id: oops\ninput: hi\nexpect: smalltalk\n")  # a mapping, not a list
    try:
        load_cases(bad)
        assert False, "expected ValueError"
    except ValueError as exc:
        assert "expected a list of cases" in str(exc)


def test_load_non_mapping_row_gives_clear_error(tmp_path):
    bad = tmp_path / "bad.yaml"
    bad.write_text("- id: oops\n  input: hi\n  expect: smalltalk\n- just a string\n")
    try:
        load_cases(bad)
        assert False, "expected ValueError"
    except ValueError as exc:
        assert "expected a mapping with id/input/expect" in str(exc)
