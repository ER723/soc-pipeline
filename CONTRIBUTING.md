# Contributing

This is a personal portfolio project documenting a working SOC escalation pipeline. It's not accepting external code contributions — the live implementation lives in a private companion repository, not here — but feedback, questions, and corrections are genuinely welcome.

## What's in this repo

This repository contains the architecture write-up, test methodology, verified evidence, and honest limitations documentation for the pipeline. It's intentionally documentation-only: there's no application code to build, install, or run here. The actual system runs on a real macOS host using Wazuh, Python, and Docker — see the linked private repository for that.

## How to contribute

**Found an issue with the documentation or test methodology?**
Open an issue describing exactly what's wrong and where. Include the file name and, if relevant, a line or section reference, so it's easy to locate and verify.

**Questions about the architecture or how something was tested?**
Open an issue — happy to explain the reasoning behind any design decision, why a particular detection technique was chosen, or how a specific test was carried out end to end.

**Spotted something inaccurate, outdated, or a broken link?**
Please flag it directly. Accuracy is the entire point of this project — every claim in the test-results and limitations documentation is meant to be independently verifiable against real evidence (a log line, a timestamped screenshot, a linked commit), not taken on faith. A factual error undermines that goal, so catching one is genuinely valuable.

## Style notes

Documentation here favors plain, direct language over marketing-style claims. Every test result cites concrete evidence rather than an unsubstantiated assertion, and every known limitation is documented honestly rather than omitted. If you're suggesting an edit, please keep that same standard: specific and checkable, not vague or promotional.

This also applies to severity and capability claims — if a detection technique is described as "escalated," that means it was verified landing in the actual alerting channel (Discord/Sheet), not merely that a rule matched in isolation. Please preserve that distinction in any suggested wording changes.

## No formal PR process

Since there's no application code in this repo to contribute to, there's no build step, test suite, or CI pipeline to satisfy before a change can be accepted. Documentation edits are reviewed for accuracy and clarity directly, typically within a few days.

## Code of conduct

Be specific, be respectful, and back up claims with evidence — the same standard this project holds itself to.
