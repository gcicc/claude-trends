"""Render the sweep payload and the usage metrics into self-contained HTML.

Pattern ported from ``02-Maintain/hangar/hangar/render.py``: JSON -> Jinja -> one
HTML file with CSS inlined, data and page decoupled.

Two pages, and a hard privacy line between them:

* ``docs/index.html`` is public. It is built from ``data/runs/<date>.json`` and the
  report index only. Nothing under ``data/usage`` is ever read for it.
* ``local/usage.html`` is gitignored. It is built from ``data/usage/`` and is never
  linked from the public page.
"""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from markupsafe import Markup, escape

TEMPLATES = Path(__file__).resolve().parent / "templates"
INDEX_LINE = re.compile(r"^- (\d{4}-\d{2}-\d{2}): \[(.+?)\]\((.+?)\)\s*(?:[—-]\s*)?(.*)$")
CODE = re.compile(r"`([^`]+)`")

# August 2026 baseline, WORKING-WITH-GREG.md section 5.
AUG = {
    "interruption_rate": 0.148,
    "ask_rejected": 0.23,
    "plan_rejected": 0.31,
    "bash_rejected": 0.011,
    "median_prompt": 66,
    "share_under_60": 0.43,
}
THIN_SAMPLE = 10


def _embed(data: dict) -> str:
    """Serialise the payload for inlining inside a <script> block.

    ``</script>`` anywhere in the data would close the block early, and ``<!--``
    opens an HTML comment inside it. Both are escaped at the JSON level, which
    leaves the parsed values identical. Headlines are user-supplied text from
    third-party feeds, so this is load-bearing, not theoretical.
    """
    text = json.dumps(data, separators=(",", ":"), allow_nan=False, default=str)
    return text.replace("<\\/", "<\\\\/").replace("</", "<\\/").replace("<!--", "\\u003c!--")


def _md(value) -> Markup:
    """Escape, then turn `code` spans into <code>. Nothing else is interpreted."""
    return Markup(CODE.sub(r"<code>\1</code>", str(escape(str(value)))))


def _env() -> Environment:
    env = Environment(loader=FileSystemLoader(TEMPLATES), autoescape=True)
    env.filters["md"] = _md
    return env


REPO_BLOB = "https://github.com/gcicc/claude-trends/blob/main/"


def load_index(path: Path) -> list[dict]:
    """Parse the rolling report index into run-history rows, newest first."""
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        match = INDEX_LINE.match(line)
        if not match:
            continue
        date, label, link, summary = match.groups()
        rows.append(
            {
                "date": date,
                "label": label,
                # Pages serves only docs/, so reports and run JSON link to the
                # repo, where GitHub renders Markdown. Resolves once pushed.
                "href": REPO_BLOB + (link[3:] if link.startswith("../") else f"reports/{link}"),
                "summary": summary,
                "legacy": link.startswith("legacy/"),
            }
        )
    return sorted(rows, key=lambda r: r["date"], reverse=True)


def latest_json(folder: Path) -> Path | None:
    files = sorted(folder.glob("*.json"))
    return files[-1] if files else None


def _common() -> dict:
    return {
        "styles": (TEMPLATES / "styles.css").read_text(encoding="utf-8"),
        "app": (TEMPLATES / "app.js").read_text(encoding="utf-8"),
        "generated": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M"),
    }


def render_public(run: dict, history: list[dict], out: Path) -> Path:
    html = (
        _env()
        .get_template("page.html.j2")
        .render(
            run=run, history=history, tiers=run.get("tiers", {}), payload=_embed(run), **_common()
        )
    )
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    return out


# ---------- usage view model ----------------------------------------------


def _pct(value: float | None) -> str:
    return "n/a" if value is None else f"{value * 100:.1f}%"


def _rejection(metrics: dict, tool: str) -> tuple[float | None, int, int]:
    calls = metrics.get("tools", {}).get(tool, 0)
    rejected = metrics.get("tool_rejections", {}).get(tool, {}).get("rejected", 0)
    return (rejected / calls if calls else None), rejected, calls


def _status(value: float | None, baseline: float, calls: int) -> tuple[str, bool]:
    if value is None:
        return "no data", False
    return ("met" if value <= baseline else "worse"), calls < THIN_SAMPLE


COACHING_SECTIONS = [
    ("adoption_gap", "Adoption gap", "Shipped features crossed with observed use. Not yet run."),
    (
        "recurring_prompts",
        "Recurring prompts (3 or more times)",
        "Each with a draft slash command or skill. Not yet run.",
    ),
    (
        "precision_misses",
        "Precision misses",
        "Prompts followed by an interruption, rejection or correction, and what each lacked. Not yet run.",
    ),
    (
        "claude_should_change",
        "What Claude should change",
        "Proposed rule or doc changes. Never auto-applied. Not yet run.",
    ),
]


def usage_view(metrics: dict, coaching: dict | None) -> dict:
    turns = metrics["prompts"] + metrics["interruptions"]
    interruption_rate = metrics["interruptions"] / turns if turns else None
    ask, ask_n, ask_calls = _rejection(metrics, "AskUserQuestion")
    plan, plan_n, plan_calls = _rejection(metrics, "ExitPlanMode")
    bash, bash_n, bash_calls = _rejection(metrics, "Bash")

    measured = [
        ["Prompts", metrics["prompts"], "150", "his turns, 30 session directories"],
        ["Interruptions per turn", _pct(interruption_rate), "14.8%", "26 / 176 turns"],
        [
            "AskUserQuestion rejected",
            f"{ask_n}/{ask_calls} ({_pct(ask)})",
            "13/57 (23%)",
            "nearly one in four asks refused",
        ],
        [
            "ExitPlanMode rejected",
            f"{plan_n}/{plan_calls} ({_pct(plan)})",
            "5/16 (31%)",
            "plans reach past what he asked",
        ],
        [
            "Bash rejected",
            f"{bash_n}/{bash_calls} ({_pct(bash)})",
            "11/1023 (1%)",
            "tool choice is fine",
        ],
        [
            "Median prompt (chars)",
            metrics["prompt_chars_median"],
            "66",
            "expects inference on mechanics",
        ],
        ["Prompts under 60 chars", _pct(metrics["prompt_share_under_60"]), "43%", ""],
        ["Median response (chars)", "not measured", "123", "verbosity is not the issue"],
    ]

    commitments = []
    for label, value, baseline, n, calls in [
        (
            "Interruptions per turn fall",
            interruption_rate,
            AUG["interruption_rate"],
            metrics["interruptions"],
            turns,
        ),
        ("AskUserQuestion rejections fall", ask, AUG["ask_rejected"], ask_n, ask_calls),
        ("ExitPlanMode rejections fall", plan, AUG["plan_rejected"], plan_n, plan_calls),
        (
            "Bash rejections stay at or below baseline",
            bash,
            AUG["bash_rejected"],
            bash_n,
            bash_calls,
        ),
    ]:
        status, thin = _status(value, baseline, calls)
        commitments.append(
            {
                "label": label,
                "target": f"at or below {_pct(baseline)}",
                "now": _pct(value),
                "n": f"{n}/{calls}",
                "status": status,
                "thin": thin,
                "source": "WORKING-WITH-GREG §5",
            }
        )

    slash_counts = metrics.get("slash_commands", {})
    installed = set(metrics.get("inventory", {}).get("commands", []))
    names = list(slash_counts) + [c for c in sorted(installed) if c not in slash_counts]
    slash = [
        [f"/{n}", slash_counts.get(n, 0), "yes" if n in installed else "built-in"]
        for n in names
        if slash_counts.get(n, 0)
    ]

    rejections = [
        [t, v["rejected"], v["calls"], _pct(v["rejected"] / v["calls"] if v["calls"] else None)]
        for t, v in metrics.get("tool_rejections", {}).items()
    ]

    coaching_present = coaching is not None
    sections = []
    for key, title, placeholder in COACHING_SECTIONS:
        sections.append(
            {"title": title, "placeholder": placeholder, "items": (coaching or {}).get(key, [])}
        )

    return {
        "measured": measured,
        "commitments": commitments,
        "slash": slash,
        "slash_total": sum(slash_counts.values()),
        "unused_commands": metrics.get("unused_commands", []),
        "skills_used": [[k, v] for k, v in metrics.get("skills_invoked_by_claude", {}).items()],
        "rejections": rejections,
        "subagent_models": [[k, v] for k, v in metrics.get("subagent_models", {}).items()],
        "subagent_types": [[k, v] for k, v in metrics.get("subagent_types", {}).items()],
        "coaching": sections,
        "coaching_present": coaching_present,
    }


def render_usage(metrics: dict, coaching: dict | None, out: Path) -> Path:
    html = (
        _env()
        .get_template("usage.html.j2")
        .render(u=metrics, view=usage_view(metrics, coaching), tiers={}, **_common())
    )
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    return out


def build(root: Path) -> list[Path]:
    """Render both pages under ``root``; returns the files written."""
    written = []
    run_file = latest_json(root / "data" / "runs")
    if run_file:
        run = json.loads(run_file.read_text(encoding="utf-8"))
        history = load_index(root / "reports" / "claude-trends-index.md")
        written.append(render_public(run, history, root / "docs" / "index.html"))
    metrics_file = root / "data" / "usage" / "usage-metrics.json"
    if metrics_file.exists():
        metrics = json.loads(metrics_file.read_text(encoding="utf-8"))
        coaching_file = root / "data" / "usage" / "coaching.json"
        coaching = (
            json.loads(coaching_file.read_text(encoding="utf-8"))
            if coaching_file.exists()
            else None
        )
        written.append(render_usage(metrics, coaching, root / "local" / "usage.html"))
    return written
