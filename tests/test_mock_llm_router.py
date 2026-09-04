import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_mock_llm_suite_passes():
    proc = subprocess.run(
        [
            sys.executable,
            str(ROOT / "run_evals.py"),
            str(ROOT / "evals" / "mock_llm.yaml"),
            "--fn",
            "examples.mock_llm_router:route",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
