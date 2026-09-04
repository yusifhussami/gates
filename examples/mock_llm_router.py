from __future__ import annotations

# Stands in for a real LLM call so you can try gates with zero setup and no
# API key. Swap this out for something like openai.chat.completions.create(...)
# once you're testing an actual model.

_CANNED = {
    "hello": "smalltalk",
    "hi there": "smalltalk",
    "what's the weather": "weather",
    "book a flight": "travel",
}


def route(text: str) -> str:
    t = text.lower().strip()
    for phrase, intent in _CANNED.items():
        if phrase in t:
            return intent
    return "unknown"
