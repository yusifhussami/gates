from pathlib import Path

from gates.load import load_cases


def test_load_intent_suite():
    path = Path(__file__).resolve().parents[1] / "evals" / "intent_routing.yaml"
    cases = load_cases(path)
    assert len(cases) == 5
    assert cases[0].id == "greet"
