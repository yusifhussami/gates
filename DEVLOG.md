eld, same idea as the `id`/`scorer`/`tags` checks from the last few days. Tried a non-string `note`:

```
>>> load_cases('/tmp/bad_note.yaml')[0].note
['known', 'flaky']
```

Loads fine, no crash. `note` isn't type-checked at all, so a list slips through even though `Case.note` is typed `str | None` — it would just print oddly in a FAIL line, not break anything. Also tried `id: ""` (empty string): loads fine too, just missing from the `where` snippet in error messages since that check uses truthiness (`row.get("id")`) instead of `is None`. Both are cosmetic, not landmines like the earlier ones, so didn't feel worth a fix on their own.

No code changed this session. 22 tests pass, hello eval 2/2, intent eval 5/5, mock_llm eval 3/3.

## 2026-09-05 (contains scorer)

Third pass at gates today, switching off load_cases for a bit. `demo_router`'s
billing case returns clean JSON, but a real LLM router might just answer in a
sentence — "sounds like a shipping question to me" — with no exact label to
match against. `exact` and `one_of` both need the whole value to match, so
that case had nowhere to go.

Added a `contains` scorer: `expect` just needs to show up somewhere in `got`.
Registered it in `load.py`'s `_SCORERS` dict next to the others, added a
`shipping` branch to `demo_router.py` that returns a full sentence, and a
matching case in `intent_routing.yaml`.

Ran the suite and immediately broke a test:

```
    def test_load_intent_suite():
        path = Path(__file__).resolve().parents[1] / "evals" / "intent_routing.yaml"
        cases = load_cases(path)
>       assert len(cases) == 5
E       assert 6 == 5
```

Forgot that test hardcodes the case count. Bumped it to 6.

Learned: any test asserting "N cases" in a yaml file breaks the moment you
add a case — worth remembering before adding more.

24 tests pass (was 22), hello eval 2/2, intent eval 6/6 (was 5/5), mock_llm
eval 3/3.

## 2026-09-06

Followed up on one of the "cosmetic, not landmines" notes from a few days back: an empty string id (`id: ''`) loads fine, but silently disappears from error messages, because the `where` snippet only shows the id when `row.get("id")` is truthy, and `''` is falsy. Reproduced it:

```
>>> load_cases('/tmp/bad.yaml')  # id: '', no expect
ValueError: /tmp/bad.yaml: case 0: missing required field 'expect'
```

No id in the message at all, even though the yaml has one (just an empty one). Changed the check from truthiness to `is not None`, so the same file now says `case 0 ('')`. Added a test in `tests/test_load.py`. Left the other note from that entry (`note` field not type-checked) alone for another day.

Also learned that this sandbox can't run `git` for anything (`git --version` alone hangs on a permission prompt that never gets answered), even though plain `python3 --version` and `ls -la <path>` go through fine. Cloned the repo into a Composio remote bash sandbox instead, made the change there, ran the real test suite and all three evals, then pushed through the GitHub API since local `git push` isn't reachable either.

25 tests pass (was 24), hello eval 2/2, intent eval 6/6, mock_llm eval 3/3.

## 2026-09-06 (again)

Main already had today's empty-id fix, so kept this small. Closed out the other loose end from a few days back: `note` wasn't type-checked at all in `load_cases`, same gap as `tags` before it got a check. A list slips through fine and just prints oddly in a FAIL line.

```
>>> load_cases('/tmp/bad_note.yaml')[0].note
['known', 'flaky']
```

Added the same kind of check the `tags` field already has: `note` must be a string or None, otherwise a clear ValueError. One test added.

26 tests pass (was 25), hello eval 2/2, intent eval 6/6, mock_llm eval 3/3.

## 2026-09-06 (once more)

Found the note-field-type-check work already sitting as a committed-but-unpushed local commit in the shared remote sandbox from an earlier session today — it had run out of turn before shipping. Re-ran the full suite and all three evals to confirm it still holds (26 tests, hello 2/2, intent 6/6, mock_llm 3/3), then pushed it through the GitHub API since local `git push` still isn't reachable from here.

Learned: the remote bash sandbox can persist a repo checkout (and unpushed commits) across sessions on the same day, so it's worth a `git log`/`git status` check right after cloning instead of assuming a fresh clone — there may already be finished work waiting to ship.

No new code this session; same 26 tests pass, hello eval 2/2, intent eval 6/6, mock_llm eval 3/3.

## 2026-09-06 (yet again)

Three sessions already touched main today, so this one is tiny. `gates/__init__.py` exported `Case`, `run_suite`, and the scorers but left out `load_cases` — the one function you actually need to turn a yaml file into cases. Nothing was broken since everything internally imports it straight from `gates.load`, just an inconsistent public surface for anyone using this as a library instead of the CLI.

Added `load_cases` to the top-level import and `__all__`. One test checking `gates.load_cases is load_cases`.

27 tests pass (was 26), hello eval 2/2, intent eval 6/6, mock_llm eval 3/3.

## 2026-09-06 (index)

Fourth session on main today. Backlog had "DEVLOG.md index at top linking each session" sitting unpicked, and this file was pushing 400 lines with no way to jump to an old entry except scrolling. Wrote a short script to pull every `## ` header and build a link list using GitHub's heading-anchor rules (lowercase, strip punctuation, spaces to hyphens), then dropped it in as an `## index` section right under the intro line.

Also found the sandbox's local checkout of this repo (a different path, left over from earlier sessions today) had drifted from `origin/main` — it had an unpushed "export load_cases" commit that duplicated work another session had already pushed under a different commit hash, plus a stray "fix devlog placeholder" commit repairing an earlier session's DEVLOG.md mishap. Didn't touch any of that; did a fresh `git clone` into a new directory instead of trusting the stale checkout, confirmed it was green (26 tests), and worked from there.

No code changed, only DEVLOG.md. 26 tests pass, hello eval 2/2, intent eval 6/6, mock_llm eval 3/3.

## 2026-09-06 (tags)

Sixth session on main today, so kept this tiny. Same family of bug as the old `note`-field gap: `tags` was checked for being a list, but never checked that each *item* in the list was a string. A yaml like `tags: [1]` loaded fine:

```
>>> load_cases('/tmp/bad_tags.yaml')[0].tags
(1, 2, 'ok')
```

Not a crash, but a quiet footgun: `run_evals.py --tags travel` filters by comparing strings, so a case tagged with an int would just never match any `--tags` filter and you'd never know why. Added a check right after the list check, one line per item, same pattern as `id`/`scorer`/`note`. One test in `tests/test_load.py`.

27 tests pass (was 26), hello eval 2/2, intent eval 6/6, mock_llm eval 3/3.

## 2026-09-06 (id)

Same shape as the tags and note gaps: `id` was checked for being hashable (a list or dict id already gave a clear error) but nothing stopped a number from sliding through, even though `Case.id` is typed `str`.

```
>>> load_cases('/tmp/bad_id.yaml')[0].id
123
```

Duplicate-id checks and `--tags` filtering both assume strings downstream, so this was one more version of the same footgun as before. Added the check right after the hashability one, same pattern as `tags`/`note`. One test in `tests/test_load.py`.

28 tests pass (was 27), hello eval 2/2, intent eval 6/6, mock_llm eval 3/3.

## 2026-09-07

Same family of bug as `id`/`tags`/`note` from yesterday: `load_cases` required an `input` field but never checked it was a string. `Case.input` is typed `str`, and `contains`/`json_keys` scorers, plus the demo routers, all assume `input` is text you can pass to a router function or `str.contains`-style check. A yaml like `input: 123` loaded fine and would only blow up later, deep inside whatever router function you passed to `--fn`, with a confusing error far from the actual mistake.

```
>>> load_cases('/tmp/bad_input.yaml')[0].input
123
```

Added the same "should be a string" check right after the `tags` check, before `note`. One test in `tests/test_load.py`, same shape as `test_load_non_string_id_gives_clear_error`.

29 tests pass (was 28), hello eval 2/2, intent eval 6/6, mock_llm eval 3/3.

## 2026-09-07 (again)

Main already had today's `input` type check, so kept this tiny. `SuiteReport.pass_rate` has been in `gates/runner.py` since the start, but `tests/test_runner.py` never once called it — `passed` and `failed` both had coverage, this one didn't.

Added two tests: an empty suite gives `1.0` (nothing to fail), and a two-case suite with one hit and one miss gives `0.5`.

31 tests pass (was 29), hello eval 2/2, intent eval 6/6, mock_llm eval 3/3.

## 2026-09-07 (scorers)

Third session on main today, so kept this tiny. `json_keys` had a test for the happy path (partial match works) but nothing for what happens when the thing you're scoring isn't valid JSON at all — `json.loads` throws inside the scorer, gets caught, and returns `False`, but no test ever walked that path.

Real case this covers: your router is supposed to return JSON but starts returning a plain string (a bug, a bad prompt change, whatever) — you want that to show up as a normal `[FAIL]`, not a crash. Added one test in `tests/test_runner.py` confirming exactly that.

32 tests pass (was 31), hello eval 2/2, intent eval 6/6, mock_llm eval 3/3.

## 2026-09-07 (one_of)

Fourth session on main today, so kept this one small too. Backlog note from an earlier session pointed at `one_of` falling back to plain `==` when `expect` isn't a list/tuple/set — that branch existed in `gates/scorers.py` since the start but had no test:

```python
def one_of(got, expect):
    if not isinstance(expect, (list, tuple, set)):
        return got == expect
    return got in expect
```

Only the list-form (`expect: [a, b]`) had a test. Added two for the fallback: a case where `expect` is a plain string and it matches, and one where it doesn't, so both sides of that `==` are covered the same way `exact` already is.

34 tests pass (was 32), hello eval 2/2, intent eval 6/6, mock_llm eval 3/3.

## 2026-09-07 (json_keys again)

Fifth session on main today, so kept this one tiny too. `json_keys` checks `isinstance(expect, dict)` and bails to `False` if it isn't, but nothing exercised that side of the check — only the "invalid json string" and "partial match" paths had tests. Passing a list as `expect` (easy yaml mistake, e.g. writing it like a `one_of` case by accident) was silently untested.

Added one test: `expect=["intent", "billing"]` against a valid `got` dict, asserting it fails instead of crashing or matching wrong.

35 tests pass (was 34), hello eval 2/2, intent eval 6/6, mock_llm eval 3/3.

## 2026-09-07 (scorer type check)

Sixth session on main today, so kept this tiny too. `load_cases` already wraps the `id` hashability check in `except TypeError`, and it turns out `scorer` has the exact same guard sitting right below it:

```python
try:
    scorer = _SCORERS.get(scorer_name)
except TypeError:
    raise ValueError(f"{where}: 'scorer' should be a plain value like a string, got {scorer_name!r}") from None
```

So `scorer: [nope]` in a yaml already gets a clear error instead of crashing on `TypeError: unhashable type: 'list'` — the code was already right, it just had zero test coverage proving it, unlike the `id` version of the same guard.

Added one test in `tests/test_load.py`, same shape as `test_load_unhashable_id_gives_clear_error`.

36 tests pass (was 35), hello eval 2/2, intent eval 6/6, mock_llm eval 3/3.

## 2026-09-08

Checked `git log` first — nothing had shipped yet today, so a normal-sized session was fine. Ran the full suite before touching anything: 36 passed.

`run_evals.py`'s `--fn` handling already gives clean errors for a bad module (`can't import '...'`) and a missing function (`'...' has no function '...'`) instead of a raw traceback — good beginner-friendly behavior. But neither path had a test, unlike the CLI's other error cases (`--tags` no-match, missing suite file, bad yaml) which `tests/test_tags.py` already covers.

Added `tests/test_fn_errors.py` with two subprocess tests: `--fn examples.nope_router:route` (bad module) and `--fn examples.hello_router:nope_fn` (missing function), each asserting exit code 2, no traceback, and the right message.

38 tests pass (was 36), hello eval 2/2, intent eval 6/6.

## 2026-09-08 (again)

Main already had a commit today, so kept this one small. `run_suite` returns a `SuiteReport`, and `run_suite` itself is importable from `gates` top level (`from gates import run_suite`), but `SuiteReport` wasn't — you'd have to reach into `gates.runner` just to type-hint the thing the function you already imported returns. Same shape as the earlier `load_cases` top-level export.

Added `SuiteReport` to `gates/__init__.py`'s imports and `__all__`, plus one test mirroring `test_load_cases_importable_from_gates_top_level`.

39 tests pass (was 38), hello eval 2/2, intent eval 6/6, mock_llm eval 3/3.

## 2026-09-08 (third)

Third session on `main` today, so kept this one small too. Went looking in `gates/load.py` for another "guard exists but has no test" gap like the recent `one_of`/`json_keys`/`scorer` ones — found two: `load_cases` raises a clear `"expected a list of cases"` error when the top-level YAML isn't a list, and a separate `"expected a mapping with id/input/expect"` error when a list item isn't a dict. Neither had a test, even though every other validation branch in that function does.

Added one test, `test_load_non_list_yaml_gives_clear_error`, covering the top-level case (a YAML file that's a mapping instead of a list). Left the per-row mapping check for a future session — didn't want to stack two new tests in one small session.

Also hit a near-miss shipping this: a probe call meant to test a parameter went out as a real commit with placeholder content and briefly clobbered `tests/test_load.py` on `main`. Caught it immediately by checking the commit response and fixed it with a follow-up commit restoring the real content. Lesson for next time: never send a real mutating GitHub call with placeholder content, even "just to test a field" — the near-miss note from 2026-09-07 said the same thing and it happened again anyway.

40 tests pass (was 39), hello eval 2/2, intent eval 6/6, mock_llm eval 3/3.

## 2026-09-08 (fourth)

Fourth session on `main` today, so kept this tiny. The last entry flagged a gap and skipped it on purpose: `load_cases` also raises a clear error when a list item isn't a mapping (`"expected a mapping with id/input/expect"`), but nothing tested that branch, only the top-level "not a list" one.

Added `test_load_non_mapping_row_gives_clear_error`: a yaml file with one good case followed by a bare string instead of a mapping, checking `load_cases` raises with that message instead of blowing up on `row.get`.

41 tests pass (was 40), hello eval 2/2, intent eval 6/6, mock_llm eval 3/3.

## 2026-09-08 (fifth)

Fifth session on `main` today, so kept this one small again. Went back through `run_evals.py`'s `--fn` handling: the bad-module and missing-function error paths already had tests (from an earlier session today), but the third branch of the same check — passing `--fn` with no colon at all, e.g. `--fn examples.hello_router` instead of `examples.hello_router:route` — had zero coverage even though the code already handles it cleanly (`Pass a function like: examples.hello_router:route`, exit code 2, no traceback).

Added `test_cli_fn_without_colon_is_clear_error` to `tests/test_fn_errors.py`, same shape as its two siblings.

Also swept `gates/scorers.py`, `gates/runner.py` (including `SuiteReport.pass_rate` and the exception-catching path in `run_suite`), and `tests/test_tags.py`'s CLI error paths — all already have direct tests, so that family of "untested guard" gaps looks genuinely closed out for now on this pass.

42 tests pass (was 41), hello eval 2/2, intent eval 6/6, mock_llm eval 3/3.

**Learned:** when a whole file (scorers.py) or whole error-path family looks done, it's worth doing one more full sweep before assuming there's nothing left — the `--fn` no-colon gap was sitting right next to two already-fixed siblings in the same file.

**Next idea:** haven't looked closely at `gates/case.py` or the YAML loading of `tags`/`note` defaults (e.g. what happens with `tags: null` vs omitted) — worth a look next session.
