# Claude Trends — SPEC

**Goal.** Make each `/claude-trends` sweep a browsable, evidence-graded web page in the HANGAR
house style, and give Greg a private measure of how he uses Claude Code, with coaching.

**Done criteria (all testable)**

1. `python run.py --render` writes `docs/index.html` from the latest `data/runs/*.json` and
   `local/usage.html` from `data/usage/`; `python run.py --usage --since D` writes
   `data/usage/usage-metrics.json`.
2. The public page shows: strip rack with evidence-tier left edges, source bus (ok/failed per
   source), run-history rail listing every report in the index (legacy ones link to their `.md`),
   retired-advice ledger, Grok tables; works in light and dark.
3. At 390 px width `scrollWidth == clientWidth` on both pages; no console errors.
4. Both pages carry the RANGER chrome snippet with `data-section="claude-trends"`.
5. `docs/index.html` contains no string from `data/usage/` (pytest: fixture prompt text and
   coaching text absent; `usage.html` not linked).
6. `local/` and `data/usage/` are gitignored; the repo has no remote.
7. `usage.py` counts are exact on a synthetic transcript (prompts, slash commands, rejections,
   interruptions, Skill calls) — pytest.
8. `ruff format`, `ruff check` and `pytest` pass; no dependency beyond jinja2.
9. `~/.claude/commands/claude-trends.md` writes absolute paths under this folder, writes the run
   JSON and renders, and has Step 9 (usage review) with proposals never auto-applied.

**Out of scope.** A cron for the sweep (it needs judgement); publishing or pushing (outward gate,
Greg's go only); auto-editing rules or docs from coaching output; any usage data on a public
surface; charts.

**Constraints.** Python 3.11+, jinja2 only. Single-file HTML with inlined CSS. Usage prompts CSV
is local-only. Render with `run.py`, not `quarto`.

**Open questions.** Is the `claude-trends` section id registered in `03-Tools/suite-nav/suite.json`
(`live: false` until the page serves 200)? Will Pages serve only `docs/`, in which case the
`../reports/*.md` links need a decision (copy reports into `docs/` or link to the repo)?
