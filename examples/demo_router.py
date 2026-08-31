"""Day-one stub router. Swap this for your real model call."""

from __future__ import annotations

import json
import re


def route(text: str) -> str | dict:
    t = text.lower().strip()

    if re.search(r"\b(hey|hi|hello|how are you)\b", t):
        return "smalltalk"
    if "forecast" in t or "weather" in t:
        return "weather"
    if "flight" in t or "lisbon" in t:
        return "travel"
    if t == "cancel it":
        return "clarify"
    if "charged twice" in t or "subscription" in t:
        return json.dumps({"intent": "billing", "urgency": "high"})
    return "unknown"
