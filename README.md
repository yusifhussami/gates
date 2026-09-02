# gates

YAML test cases for LLM routing. Point at your router function, run it, see pass/fail.

## setup

```bash
python3 -m venv .venv
source .venv/bin/activate    # windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Need Python 3.9+. Check with `python3 --version`.

## run

```bash
PYTHONPATH=. python run_evals.py evals/hello.yaml --fn examples.hello_router:route
```

Windows PowerShell:

```powershell
$env:PYTHONPATH="."; python run_evals.py evals/hello.yaml --fn examples.hello_router:route
```

You want `[ok]` on each line and `2/2 passed` at the bottom.

Five-case example:

```bash
PYTHONPATH=. python run_evals.py evals/intent_routing.yaml --fn examples.demo_router:route
```

## add a case

Edit `evals/hello.yaml`:

```yaml
- id: says_hi
  input: "hello"
  expect: smalltalk
```

Re-run the command. Wrong answer → `[FAIL]` with what your router actually returned.

Multiple valid answers: `scorer: one_of` and a list in `expect`. Partial JSON: `scorer: json_keys`. See `evals/intent_routing.yaml`.

## run a subset

Tag cases in the yaml:

```yaml
- id: book_flight
  input: "find me a flight to lisbon"
  expect: travel
  tags: [travel]
```

Then run just those:

```bash
PYTHONPATH=. python run_evals.py evals/intent_routing.yaml --fn examples.demo_router:route --tags travel
```

Comma-separate to match more than one tag: `--tags travel,billing`.

## tests

```bash
PYTHONPATH=. pytest
```

## files

```
evals/        yaml cases
examples/     sample routers
gates/        loader, runner, scorers
run_evals.py  cli
```

## why bother

You tweak a prompt, routing drifts, nobody notices until a user hits a weird message. Same idea as unit tests.

See `VOICE.md` for how we write commits and notes in this repo.

MIT
