from __future__ import annotations

from pathlib import Path

import yaml

from gates.case import Case
from gates.scorers import exact, json_keys, one_of

_SCORERS = {
    "exact": exact,
    "one_of": one_of,
    "json_keys": json_keys,
}

_REQUIRED_FIELDS = ("id", "input", "expect")


def load_cases(path: str | Path) -> list[Case]:
    raw = yaml.safe_load(Path(path).read_text())
    if not isinstance(raw, list):
        raise ValueError(f"{path}: expected a list of cases")

    cases: list[Case] = []
    for i, row in enumerate(raw):
        where = f"{path}: case {i}" + (f" ({row.get('id')!r})" if isinstance(row, dict) and row.get("id") else "")

        if not isinstance(row, dict):
            raise ValueError(f"{where}: expected a mapping with id/input/expect, got {row!r}")

        for field in _REQUIRED_FIELDS:
            if field not in row:
                raise ValueError(f"{where}: missing required field '{field}'")

        scorer_name = row.get("scorer", "exact")
        scorer = _SCORERS.get(scorer_name)
        if scorer is None:
            raise ValueError(f"{where}: unknown scorer '{scorer_name}', pick one of {list(_SCORERS)}")

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
