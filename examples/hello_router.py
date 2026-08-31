"""Smallest possible router — good starting point for your first eval run."""


def route(text: str) -> str:
    t = text.lower().strip()
    if t in ("hi", "hello", "hey", "hey there"):
        return "smalltalk"
    return "other"
