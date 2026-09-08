import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_cli_bad_module_is_clear_error():
    proc = subprocess.run(
        [
            sys.executable,
            str(ROOT / "run_evals.py"),
            str(ROOT / "evals" / "hello.yaml"),
            "--fn",
            "examples.nope_router:route",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 2
    assert "Traceback" not in proc.stderr
    assert "can't import 'examples.nope_router'" in proc.stderr


def test_cli_missing_function_is_clear_error():
    proc = subprocess.run(
        [
            sys.executable,
            str(ROOT / "run_evals.py"),
            str(ROOT / "evals" / "hello.yaml"),
            "--fn",
            "examples.hello_router:nope_fn",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 2
    assert "Traceback" not in proc.stderr
    assert "'examples.hello_router' has no function 'nope_fn'" in proc.stderr


def test_cli_fn_without_colon_is_clear_error():
    proc = subprocess.run(
        [
            sys.executable,
            str(ROOT / "run_evals.py"),
            str(ROOT / "evals" / "hello.yaml"),
            "--fn",
            "examples.hello_router",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 2
    assert "Traceback" not in proc.stderr
    assert "Pass a function like: examples.hello_router:route" in proc.stderr


def test_cli_fn_not_callable_is_clear_error():
    proc = subprocess.run(
        [
            sys.executable,
            str(ROOT / "run_evals.py"),
            str(ROOT / "evals" / "hello.yaml"),
            "--fn",
            "examples.hello_router:__name__",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 2
    assert "Traceback" not in proc.stderr
    assert "'__name__' in 'examples.hello_router' isn't a function, it's a str" in proc.stderr
