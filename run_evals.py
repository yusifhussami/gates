#!/usr/bin/env python3

from __future__ import annotations

import argparse
import importlib
import sys
from pathlib import Path

from gates.case import Case
from gates.load import load_cases
from gates.runner import run_suite


def filter_by_tags(cases: list[Case], tags_arg: str) -> list[Case]:
    wanted = {t.strip() for t in tags_arg.split(",") if t.strip()}
    return [c for c in cases if set(c.tags) & wanted]


def main() -> int:
    p = argparse.ArgumentParser(
        description="Run eval cases from a YAML file against your router function.",
    )
    p.add_argument("suite", type=Path, help="path to YAML cases")
    p.add_argument(
        "--fn",
        required=True,
        help="dotted path to callable, e.g. examples.demo_router:route",
    )
    p.add_argument(
        "--tags",
        help="comma-separated tags, e.g. --tags baseline,billing — only runs cases with a matching tag",
    )
    args = p.parse_args()

    mod_name, _, attr = args.fn.partition(":")
    if not attr:
        print("Pass a function like: examples.hello_router:route", file=sys.stderr)
        return 2

    try:
        mod = importlib.import_module(mod_name)
    except ImportError as exc:
        print(f"can't import '{mod_name}': {exc}", file=sys.stderr)
        return 2

    try:
        fn = getattr(mod, attr)
    except AttributeError:
        print(f"'{mod_name}' has no function '{attr}'", file=sys.stderr)
        return 2

    try:
        cases = load_cases(args.suite)
    except FileNotFoundError:
        print(f"can't find suite file '{args.suite}'", file=sys.stderr)
        return 2

    if args.tags:
        cases = filter_by_tags(cases, args.tags)
        if not cases:
            print(f"no cases match --tags {args.tags!r}", file=sys.stderr)
            return 2

    report = run_suite(cases, fn)

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
    if report.failed:
        print("check expect in the yaml matches what your router returns", file=sys.stderr)
    return 0 if report.failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
