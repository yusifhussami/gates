#!/usr/bin/env python3
"""Run a YAML eval suite against a callable."""

from __future__ import annotations

import argparse
import importlib
import sys
from pathlib import Path

from gates.load import load_cases
from gates.runner import run_suite


def main() -> int:
    p = argparse.ArgumentParser(description="Run gates eval suite")
    p.add_argument("suite", type=Path, help="path to YAML cases")
    p.add_argument(
        "--fn",
        required=True,
        help="dotted path to callable, e.g. examples.demo_router:route",
    )
    args = p.parse_args()

    mod_name, _, attr = args.fn.partition(":")
    if not attr:
        print("use module:callable", file=sys.stderr)
        return 2

    mod = importlib.import_module(mod_name)
    fn = getattr(mod, attr)

    report = run_suite(load_cases(args.suite), fn)

    for r in report.results:
        mark = "ok" if r.passed else "FAIL"
        line = f"[{mark}] {r.case.id}"
        if not r.passed:
            if r.error:
                line += f"  error={r.error}"
            else:
                line += f"  got={r.got!r} expect={r.case.expect!r}"
        print(line)

    print(f"\n{report.passed}/{len(report.results)} passed")
    return 0 if report.failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
