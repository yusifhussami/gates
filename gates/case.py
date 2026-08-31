from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable


Scorer = Callable[[Any, Any], bool]


@dataclass(frozen=True)
class Case:
    id: str
    input: str
    expect: Any
    scorer: Scorer = field(repr=False)
    tags: tuple[str, ...] = ()
    note: str | None = None


@dataclass
class Result:
    case: Case
    got: Any
    passed: bool
    error: str | None = None
