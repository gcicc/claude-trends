---
name: claude-trends
type: maintain
category: building
tier: 02-Maintain
updated: 2026-11-11
---
# Claude Trends — next steps

## Where this stands

Built 2026-11-11 (Phase 1 of the claude-trends/suite plan). `python run.py` renders the public
`docs/index.html` from `data/runs/2026-10-29.json` (hand-extracted seed from the 10-29 delta
report) and the local-only `local/usage.html` from `data/usage/`. Reports, roster and the usage
script were moved here; `/claude-trends` was edited to use absolute paths, write the run JSON and
run Step 9. Local git only, no remote, nothing published.

## Next task

Greg views both pages (light, dark, 390 px), then decides on the outward gate: create
`gcicc/claude-trends`, enable Pages, register the section in `suite-nav/suite.json`.
Then run `/claude-trends` end to end once to prove the new Step 6 and Step 9 paths.

## Blockers

- Pages serves only `docs/`, so the `../reports/*.md` links do not resolve there; decide whether
  to copy reports into `docs/` or link to the repo.
- `CAPABILITIES.md` entry and `mirror_dotclaude.py` run still to do (lead).

## What keeps this current

`/claude-trends` Step 6 writes `data/runs/<date>.json` and runs `python run.py --render`; Step 7
adds the index line; Step 9 refreshes `data/usage/`. No schedule: the sweep needs judgement.
