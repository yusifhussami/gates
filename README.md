# gates

**A tiny Python project to check if your AI router picks the right answer.**

No ML degree needed. If you can run a few terminal commands and edit a text file, you can use this.

---

## What problem does this solve?

Imagine you built a chatbot that decides what to do with each message:

- "What's the weather?" → call the weather tool
- "Hey!" → small talk, no tool
- "Cancel my order" → hand off to support

You change the prompt on Monday. By Friday, "cancel it" starts routing to the wrong place — and nobody notices until a user complains.

**gates** lets you write down example messages and the answer you expect. Run one command. See green (pass) or red (fail).

Think of it like unit tests, but for routing decisions.

---

## What you need first

1. **Python 3.9 or newer** installed on your computer.
2. A terminal (Terminal on Mac, PowerShell on Windows).

Check Python is installed:

```bash
python3 --version
```

You should see something like `Python 3.11.x`. If that command fails, install Python from [python.org](https://www.python.org/downloads/) first.

---

## Setup (copy and paste)

Open a terminal in this folder (the one that contains `README.md`).

**Step 1 — create a virtual environment** (keeps packages isolated):

```bash
python3 -m venv .venv
```

**Step 2 — turn it on:**

Mac / Linux:

```bash
source .venv/bin/activate
```

Windows:

```bash
.venv\Scripts\activate
```

You should see `(.venv)` at the start of your terminal line.

**Step 3 — install dependencies:**

```bash
pip install -r requirements.txt
```

That's it. Setup done.

---

## Your first run (2 minutes)

We ship a tiny example router in `examples/hello_router.py`. It only knows two tricks: greetings and everything else.

Run the hello eval suite:

```bash
PYTHONPATH=. python run_evals.py evals/hello.yaml --fn examples.hello_router:route
```

**On Windows (PowerShell), use this instead:**

```powershell
$env:PYTHONPATH="."; python run_evals.py evals/hello.yaml --fn examples.hello_router:route
```

You should see:

```
[ok] says_hi
[ok] not_weather

2/2 passed
```

If both lines say `[ok]`, everything works.

---

## Run the full test suite

```bash
PYTHONPATH=. pytest
```

(Windows: `$env:PYTHONPATH="."; pytest`)

You should see something like `8 passed`. That means the project itself is healthy.

---

## Try the bigger example

Once hello works, try the intent-routing demo (5 cases, closer to a real app):

```bash
PYTHONPATH=. python run_evals.py evals/intent_routing.yaml --fn examples.demo_router:route
```

---

## How to write your own test case

Open `evals/hello.yaml`. Each block is one test:

```yaml
- id: says_hi          # name you pick — shows up in the report
  input: "hello"       # the message you send to your router
  expect: smalltalk    # the answer you want back
```

Add a new case, save the file, run the command again. If your router returns something different, you'll see `[FAIL]` with what it actually returned.

### Optional: allow more than one correct answer

```yaml
- id: vague_cancel
  input: "cancel it"
  expect: [clarify, support]
  scorer: one_of
```

### Optional: check part of a JSON response

```yaml
- id: billing
  input: "I was charged twice"
  expect:
    intent: billing
    urgency: high
  scorer: json_keys
```

---

## Project layout (where things live)

```
gates/
├── evals/              ← your test cases (YAML files)
├── examples/           ← sample routers to test against
├── gates/              ← the small library (runner, scorers)
├── tests/              ← tests for the library itself
├── run_evals.py        ← the script you run
└── requirements.txt    ← packages to install
```

---

## Words we use

| Word | Meaning |
|------|---------|
| **Router** | A function that reads a user message and returns a label (e.g. `weather`, `smalltalk`). |
| **Eval** | One input + expected output pair. |
| **Scorer** | How we decide pass/fail. Default: exact match. |
| **Suite** | A YAML file full of evals. |

---

## What's built so far (day 1)

- Runner + three scorers: `exact`, `one_of`, `json_keys`
- Two example suites: `hello.yaml` (start here) and `intent_routing.yaml`
- Pytest coverage

**Not built yet:** plugging in a real LLM API, HTML reports, filtering by tags.

---

## Something broke?

| Problem | Fix |
|---------|-----|
| `python3: command not found` | Install Python from python.org |
| `No module named 'yaml'` | Run `pip install -r requirements.txt` again (with venv active) |
| `No module named 'gates'` | Add `PYTHONPATH=.` before the command (see examples above) |
| All tests fail after you edited a router | That's the point — fix the router or update the YAML expect value |

---

## Why this exists

Routing is where a lot of AI apps break in production — not on the demo path, but on boring edge cases. If you can't re-run the same checks after every prompt change, you're guessing.

---

## License

MIT
