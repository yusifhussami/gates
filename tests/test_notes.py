import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_cli_shows_note_on_failure(tmp_path):
    suite = tmp_path / "notes.yaml"
    suite.write_text(
        "- id: bad_guess\n"
        "  input: whatever\n"
        "  expect: not_gonna_match\n"
        "  note: known flaky, ok to ignore for now\n"
    )
    proc = subprocess.run(
        [
            sys.executable,
            str(ROOT / "run_evals.py"),
            str(suite),
            "--fn",
            "examples.hello_router:route",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert "FAIL" in proc.stdout
    assert "note='known flaky, ok to ignore for now'" in proc.stdout
