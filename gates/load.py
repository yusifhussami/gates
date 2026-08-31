from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from gates.case import Case
from gates.scorers import exact, json_keys, one_of

_SCORERS = {
    "exact": exact,
    "one_of": one_of,
    "json_keys": json_keys,
}


def load_cases(path: str | Path) -> list[Case]:
    raw = yaml.safe_load(Path(path).read_text())
    if not isinstance(raw, list):
        raise ValueError(f"{path}: expected a list of cases")

    cases: list[Case] = []
    for row in raw:
        scorer_name = row.get("scorer", "exact")
        scorer = _SCORERS.get(scorer_name)
        if scorer is None:
            raise ValueError(f"unknown scorer: {scorer_name}")

        cases.append(
            Case(
                id=row["id"],
                input=row["input"],
                expect=row["expect"],
                scorer=scorer,
                tags=tuple(row.get("tags", [])),
                note=row.get("note"),
            )
        )
    return cases
