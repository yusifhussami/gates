# How we write in this repo

Read this before every commit, DEVLOG entry, or README edit.

## Commit messages

Lowercase. Short. No colons with laundry lists.

| skip | use instead |
|------|-------------|
| `make project beginner-friendly: hello example, requirements.txt, clearer README` | `hello example and requirements.txt` |
| `Add comprehensive eval harness with robust scoring` | `add json_keys scorer` |
| `Enhance developer experience with improved documentation` | `readme install steps` |
| `Implement feature X and refactor Y` | pick one: `tag filter` or `fix loader crash` |

One line. Under ~50 chars when you can. Imperfect grammar is fine.

## DEVLOG.md

Write like you're explaining to a friend over coffee, not presenting to a panel.

| skip | use instead |
|------|-------------|
| **Tried:** I embarked on implementing tag filtering... | tried adding `--tags` to run_evals.py |
| **Learned:** This underscores the importance of... | learned argparse eats unknown flags before your code runs |
| Bullet stacks with bold labels everywhere | short paragraphs. paste the actual error. |

Include the real terminal output when something breaks. Typos ok.

## README

- Short sentences.
- No "leverage", "robust", "comprehensive", "delve", "excited to share", "game-changer".
- No "Day N status" headers unless it's literally a build log.
- If a sentence sounds like LinkedIn, delete it.

## Self-check (10 seconds)

Read it out loud. If you wouldn't send it in a Slack DM to a teammate, rewrite.
