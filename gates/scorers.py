from __future__ import annotations

import json
from typing import Any


def exact(got: Any, expect: Any) -> bool:
    return got == expect


def one_of(got: Any, expect: Any) -> bool:
    if not isinstance(expect, (list, tuple, set)):
        return got == expect
    return got in expect


def contains(got: Any, expect: Any) -> bool:
    if not isinstance(got, str):
        return False
    return str(expect) in got


def json_keys(got: Any, expect: Any) -> bool:
    if isinstance(got, str):
        try:
            got = json.loads(got)
        except json.JSONDecodeError:
            return False
    if not isinstance(got, dict) or not isinstance(expect, dict):
        return False
    for key, val in expect.items():
        if key not in got:
            return False
        if got[key] != val:
            return False
    return True
