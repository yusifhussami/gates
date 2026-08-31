# gates

Regression gates for LLM routing decisions.

Most teams test prompts by eyeballing a few examples. That works until you change the system prompt and three edge cases silently break. This is a small harness for keeping those decisions honest.

## What it does

- Define cases in YAML (`input`, `expect`, optional `scorer`)
- Point at any Python callable (your router, classifier, tool picker)
- Get a pass/fail report you can run in CI

## Day 1 status

- Core runner + three scorers (`exact`, `one_of`, `json_keys`)
- Sample intent-routing eval suite (5 cases)
- Stub router in `examples/demo_router.py`
- Pytest coverage for loader, runner, and the demo suite

Not done yet: LLM adapter, tag filtering, HTML report, CLI install entrypoint.

## Quick start

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"

pytest
python run_evals.py evals/intent_routing.yaml --fn examples.demo_router:route
```

## Case format

```yaml
- id: book_flight
  input: "find me a flight to lisbon next friday"
  expect: travel
  tags: [baseline, travel]

- id: ambiguous_cancel
  input: "cancel it"
  expect: [clarify, support]
  scorer: one_of
```

## Why this exists

Routing is where a lot of agent systems fail in production — not on the flashy demo path, but on the boring ones: billing complaints, ambiguous cancels, smalltalk that should not hit your tools. If you cannot regression-test that layer, you do not really own it.

## License

MIT
