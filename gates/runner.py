from __future__ import annotations

from collections.abc import Callable, Iterable
from dataclasses import dataclass

from gates.case import Case, Result


@dataclass
class SuiteReport:
    results: list[Result]

    @property
    def passed(self) -> int:
        return sum(1 for r in self.results if r.passed)

    @property
    def failed(self) -> int:
        return len(self.results) - self.passed

    @property
    def pass_rate(self) -> float:
        if not self.results:
            return 1.0
        return self.passed / len(self.results)


def run_suite(cases: Iterable[Case], fn: Callable[[str], Any]) -> SuiteReport:
    results: list[Result] = []
    for case in cases:
        try:
            got = fn(case.input)
            ok = case.scorer(got, case.expect)
            results.append(Result(case=case, got=got, passed=ok))
        except Exception as exc:  # noqa: BLE001 — eval harness should keep going
            results.append(
                Result(case=case, got=None, passed=False, error=str(exc))
            )
    return SuiteReport(results=results)
