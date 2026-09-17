# Contributing

This is a personal portfolio project documenting a working SOC escalation pipeline. The live implementation lives in a private companion repository, but this repo does have its own real content: documentation, a link-integrity test suite, and CI — genuine contributions and corrections are welcome.

## What's in this repo

This repository contains the architecture write-up, test methodology, verified evidence, and honest limitations documentation for the pipeline, plus a small automated test (`test_links.py`) that verifies every internal markdown link actually resolves — a real, recurring problem this project has hit more than once.

## Setup

```bash
git clone https://github.com/ER723/soc-pipeline.git
cd soc-pipeline
pip install -r requirements.txt
```

No other setup is needed — there's no application code to build or run, just the link-checker test and the documentation itself.

## Code style

Python code (currently just `test_links.py`) is linted and formatted with [ruff](https://docs.astral.sh/ruff/), configured in `ruff.toml`. Run it before submitting any change:

```bash
ruff check .
```

CI runs this automatically on every push and pull request — a failing lint check will block the PR from merging.

## Running tests

```bash
pytest test_links.py -v
```

This checks that every relative markdown link across `README.md` and `docs/*.md` points to a file that actually exists. If you add or move a doc file, run this locally before pushing to catch a broken link early.

## Pull request workflow

1. Fork the repository (or, if you have write access, create a branch directly: `git checkout -b fix/short-description`)
2. Make your change
3. Run both `ruff check .` and `pytest test_links.py -v` locally — both must pass
4. Push your branch and open a pull request against `main`
5. CI (link check + CodeQL) runs automatically on the PR — wait for it to pass before requesting a look
6. Once checks are green, the PR can be merged

This is the same process the repo's own automated dependency updates (via Dependabot) go through — every change, human or automated, gets the same CI verification before merging.

## Style notes

Documentation here favors plain, direct language over marketing-style claims. Every test result cites concrete evidence rather than an unsubstantiated assertion, and every known limitation is documented honestly rather than omitted. If you're suggesting an edit, please keep that same standard: specific and checkable, not vague or promotional.

This also applies to severity and capability claims — if a detection technique is described as "escalated," that means it was verified landing in the actual alerting channel (Discord/Sheet), not merely that a rule matched in isolation. Please preserve that distinction in any suggested wording changes.

## Code of conduct

Be specific, be respectful, and back up claims with evidence — the same standard this project holds itself to.
