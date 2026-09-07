from gates import contains, exact, json_keys, one_of
from gates.case import Case
from gates.runner import run_suite


def test_exact_match():
    c = Case(id="a", input="x", expect="yes", scorer=exact)
    report = run_suite([c], lambda _: "yes")
    assert report.passed == 1


def test_exact_miss():
    c = Case(id="a", input="x", expect="yes", scorer=exact)
    report = run_suite([c], lambda _: "no")
    assert report.failed == 1


def test_one_of_accepts_alternate():
    c = Case(id="a", input="x", expect=["a", "b"], scorer=one_of)
    report = run_suite([c], lambda _: "b")
    assert report.passed == 1


def test_contains_matches_substring():
    c = Case(id="a", input="x", expect="shipping", scorer=contains)
    report = run_suite([c], lambda _: "sounds like a shipping question")
    assert report.passed == 1


def test_contains_rejects_non_string_got():
    c = Case(id="a", input="x", expect="shipping", scorer=contains)
    report = run_suite([c], lambda _: {"intent": "shipping"})
    assert report.failed == 1


def test_json_keys_partial():
    c = Case(
        id="a",
        input="x",
        expect={"intent": "billing", "urgency": "high"},
        scorer=json_keys,
    )
    payload = '{"intent": "billing", "urgency": "high", "extra": 1}'
    report = run_suite([c], lambda _: payload)
    assert report.passed == 1


def test_runner_catches_exceptions():
    c = Case(id="boom", input="x", expect="y", scorer=exact)

    def bad(_):
        raise RuntimeError("kaboom")

    report = run_suite([c], bad)
    assert report.failed == 1
    assert report.results[0].error == "kaboom"


def test_pass_rate_empty_suite():
    report = run_suite([], lambda _: "y")
    assert report.pass_rate == 1.0


def test_pass_rate_reflects_mixed_results():
    a = Case(id="a", input="hit", expect="yes", scorer=exact)
    b = Case(id="b", input="miss", expect="yes", scorer=exact)
    report = run_suite([a, b], lambda text: "yes" if text == "hit" else "no")
    assert report.pass_rate == 0.5


def test_json_keys_rejects_invalid_json_string():
    c = Case(id="a", input="x", expect={"intent": "billing"}, scorer=json_keys)
    report = run_suite([c], lambda _: "not valid json")
    assert report.failed == 1


def test_one_of_falls_back_to_exact_when_expect_not_a_list():
    c = Case(id="a", input="x", expect="yes", scorer=one_of)
    report = run_suite([c], lambda _: "yes")
    assert report.passed == 1


def test_one_of_rejects_when_expect_not_a_list_and_got_differs():
    c = Case(id="a", input="x", expect="yes", scorer=one_of)
    report = run_suite([c], lambda _: "no")
    assert report.failed == 1
