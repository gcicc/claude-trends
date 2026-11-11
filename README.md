# Claude Trends

Turns `/claude-trends` sweep output into a web page, plus a local-only usage review.
HANGAR pattern: JSON → Jinja → one self-contained HTML file; data and page are decoupled.

| Page | Built from | Public? |
|---|---|---|
| `docs/index.html` | latest `data/runs/*.json` + `reports/claude-trends-index.md` | yes |
| `local/usage.html` | `data/usage/usage-metrics.json` (+ optional `coaching.json`) | **never** — gitignored |

The public render path never reads `data/usage/` (ADR 0001, enforced by a test).

## Commands

```
python run.py                              # --usage (last 30 days) then --render
python run.py --usage --since 2026-10-12   # measure transcripts into data/usage/
python run.py --render                     # docs/index.html and local/usage.html
python -m ruff format . && python -m ruff check .
python -m pytest -q
```

Python 3.11+, jinja2 only. Reports link to `../reports/*.md` relative to `docs/`, so those
links work locally and on a repo browser, but not on a Pages site that serves only `docs/`.

## Layout

```
run.py                         driver
claude_trends/usage.py         transcripts -> usage-metrics.json + usage-prompts.csv
claude_trends/render.py        both pages; _embed copied verbatim from hangar
claude_trends/templates/       styles.css (HANGAR tokens), page / usage / base / macros, app.js (theme toggle)
roster.csv                     Anthropic-staff roster read by /claude-trends Step 2
data/runs/<date>.json          one sweep payload per run (schema below)
data/usage/                    gitignored: usage-metrics.json, usage-prompts.csv, coaching.json
reports/                       delta reports (.md) + claude-trends-index.md; reports/legacy/ pre-series files
```

## `data/runs/<date>.json` schema (version 1)

An **item** is `{"text": str, "tier": <tier>, "src": [source ids]}`. `text` may contain
`` `code` `` spans; nothing else is interpreted. Source ids are bus ids (`newsroom`) or YouTube
video ids.

**Tiers** (drive the strip's left-edge colour): `P` Anthropic primary file · `OV` official-channel
video · `SV-h` staff talk, human captions · `SV-a` staff talk, auto-captioned · `M` description-only
metadata · Grok comparison: `vendor`, `affiliated`, `independent`, `sentiment` · `unverified`.
The file carries a `tiers` map of tier → description, used for tooltips.

```
schema            1
meta              date, baseline, baseline_note, videos, videos_note,
                  changelog {from, to, versions, note}, headline, report (relative link to the .md)
tiers             {tier: description}
sources[]         source bus: {id, name, fetched_at, status: ok|failed|unchanged, note}
sections
  exec_summary[]        items
  features[]            {area, items[]}      grouped by area
  workflows[]           items
  tools[]               items
  github                {window, rows[{repo, stars, age_days, licence, what, windows, leaves,
                         overlap, verdict}], anomalies[] items}
  applications[]        items
  pricing[]             {item, change, tier, src[]}      pricing_note: item (optional)
  consensus_shifts      {note, items[]}
  contradictions        {note, items[{claim, status: retired|flagged|note, text, tier, src[]}]}
                        the retired-advice ledger
  grok                  {mapping, unverified[] items, tier_key,
                         pairings[{id, title, note?, columns[], tier_col|null, rows[[cell]]}],
                         changed, contradicted, bottom_line}
  roster_changes[]      {name, change, evidence}
  sources_table[]       {id, title, channel, speaker, date, strength, tier}   sources_note
  methodology[]         strings
```

The run-history rail comes from `reports/claude-trends-index.md`, one line per sweep
(`- YYYY-MM-DD: [label](file.md) — summary`). Links under `legacy/` are marked as legacy.

## `data/usage/coaching.json` (optional, written by Step 9)

```
{"adoption_gap": [..], "recurring_prompts": [..], "precision_misses": [..],
 "claude_should_change": [..]}      each item: {text, evidence_count, action}
```

## What keeps this current

`/claude-trends` writes the run JSON and runs `python run.py --render`; Step 9 refreshes the
usage metrics. Nothing is scheduled: the sweep needs judgement. Seed run `2026-10-29.json` was
hand-extracted from `reports/claude-trends-2026-10-29-delta.md`.
