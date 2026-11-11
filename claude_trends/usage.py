"""Measure how Greg uses Claude Code, from the raw session transcripts.

Deterministic counts only -- no judgement. The claude-trends command feeds the
output to a subagent, which turns the counts into coaching; the counts
themselves must be reproducible run to run so the trend means something.

Reads top-level session JSONL under ~/.claude/projects/*/ (subagent transcripts
are excluded: they contain no human turns). Claude Code deletes transcripts
older than ``cleanupPeriodDays`` (default 30), so the window cannot reach back
further than what is on disk; ``files_oldest`` in the output says how far it got.

    python run.py --usage --since 2026-10-29        # writes data/usage/
    python -m claude_trends.usage --since 2026-10-29 --out <dir>

Writes ``<dir>/usage-metrics.json`` and ``<dir>/usage-prompts.csv``. The CSV
holds Greg's own prompt text: it stays local and is never published.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import statistics
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

CLAUDE = Path.home() / ".claude"
TRANSCRIPTS = CLAUDE / "projects"
DROPBOX = str(Path.home() / "Dropbox").replace("\\", "/")

REJECTED = "doesn't want to proceed with this tool use"
INTERRUPTED = "[Request interrupted by user"
COMMAND = re.compile(r"<command-name>/?([^<\s]+)</command-name>")
# User-role text that the harness wrote, not Greg.
HARNESS_PREFIXES = (
    "<command-",
    "<local-command",
    "<system-reminder>",
    "<task-notification>",
    "<bash-",
    "Caveat:",
    INTERRUPTED,
    "This session is being continued",
)
SHORT_PROMPT = 60
PROMPT_CSV_CHARS = 400


def project_of(cwd: str) -> str:
    path = cwd.replace("\\", "/")
    if path.lower().startswith(DROPBOX.lower()):
        return path[len(DROPBOX) :].strip("/") or "Dropbox"
    return path


def text_of(content) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "\n".join(
            b.get("text", "") for b in content if isinstance(b, dict) and b.get("type") == "text"
        )
    return ""


def has_tool_result(content) -> bool:
    return isinstance(content, list) and any(
        isinstance(b, dict) and b.get("type") == "tool_result" for b in content
    )


def parse_ts(value: str) -> datetime | None:
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (AttributeError, ValueError):
        return None


def inventory() -> dict[str, list[str]]:
    commands = sorted(p.stem for p in (CLAUDE / "commands").glob("*.md"))
    skills = (
        sorted(
            p.name
            for p in (CLAUDE / "skills").iterdir()
            if p.is_dir() and (p / "SKILL.md").exists()
        )
        if (CLAUDE / "skills").is_dir()
        else []
    )
    return {"commands": commands, "skills": skills}


def scan(since: datetime) -> tuple[dict, list[dict]]:
    tools: Counter = Counter()
    rejected: Counter = Counter()
    slash: Counter = Counter()
    skills_by_claude: Counter = Counter()
    agents: Counter = Counter()
    agent_models: Counter = Counter()
    models: Counter = Counter()
    projects: Counter = Counter()
    sessions: set[str] = set()
    prompts: list[dict] = []
    interruptions = 0
    files_oldest: datetime | None = None
    files_scanned = 0

    for path in sorted(TRANSCRIPTS.glob("*/*.jsonl")):
        files_scanned += 1
        tool_names: dict[str, str] = {}
        with path.open(encoding="utf-8", errors="replace") as handle:
            for line in handle:
                try:
                    record = json.loads(line)
                except json.JSONDecodeError:
                    continue
                ts = parse_ts(record.get("timestamp", ""))
                if ts is None:
                    continue
                if files_oldest is None or ts < files_oldest:
                    files_oldest = ts
                if ts < since or record.get("isSidechain"):
                    continue
                kind = record.get("type")
                message = record.get("message")
                if kind not in {"user", "assistant"} or not isinstance(message, dict):
                    continue
                content = message.get("content")
                session = record.get("sessionId", path.stem)

                if kind == "assistant":
                    if message.get("model") and message["model"] != "<synthetic>":
                        models[message["model"]] += 1
                    for block in content if isinstance(content, list) else []:
                        if not isinstance(block, dict) or block.get("type") != "tool_use":
                            continue
                        name = block.get("name", "?")
                        tool_names[block.get("id", "")] = name
                        tools[name] += 1
                        args = block.get("input") or {}
                        if name == "Skill":
                            skills_by_claude[args.get("skill", "?")] += 1
                        elif name in {"Agent", "Task"}:
                            agents[args.get("subagent_type", "general-purpose")] += 1
                            agent_models[args.get("model", "inherit")] += 1
                    continue

                # user records: tool results, harness text, or Greg
                if has_tool_result(content):
                    for block in content:
                        if (
                            isinstance(block, dict)
                            and block.get("type") == "tool_result"
                            and REJECTED in json.dumps(block.get("content", ""))
                        ):
                            rejected[tool_names.get(block.get("tool_use_id", ""), "?")] += 1
                    continue
                if record.get("isMeta"):
                    continue
                text = text_of(content).strip()
                if not text:
                    continue
                for name in COMMAND.findall(text):
                    slash[name] += 1
                if text.startswith(INTERRUPTED):
                    interruptions += 1
                    continue
                if text.startswith(HARNESS_PREFIXES):
                    continue
                sessions.add(session)
                project = project_of(record.get("cwd", ""))
                projects[project] += 1
                prompts.append(
                    {
                        "ts": ts.isoformat(timespec="minutes"),
                        "session": session[:8],
                        "project": project,
                        "chars": len(text),
                        "text": " ".join(text.split())[:PROMPT_CSV_CHARS],
                    }
                )

    lengths = [p["chars"] for p in prompts]
    inv = inventory()
    used = set(slash) | set(skills_by_claude)
    metrics = {
        "window_since": since.date().isoformat(),
        "generated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "files_scanned": files_scanned,
        "files_oldest": files_oldest.date().isoformat() if files_oldest else None,
        "sessions": len(sessions),
        "prompts": len(prompts),
        "prompt_chars_median": statistics.median(lengths) if lengths else None,
        "prompt_share_under_60": round(sum(n < SHORT_PROMPT for n in lengths) / len(lengths), 3)
        if lengths
        else None,
        "interruptions": interruptions,
        "interruptions_per_prompt": round(interruptions / len(prompts), 3) if prompts else None,
        "slash_commands": dict(slash.most_common()),
        "skills_invoked_by_claude": dict(skills_by_claude.most_common()),
        "tools": dict(tools.most_common()),
        "tool_rejections": {
            name: {"rejected": n, "calls": tools.get(name, 0)} for name, n in rejected.most_common()
        },
        "subagent_types": dict(agents.most_common()),
        "subagent_models": dict(agent_models.most_common()),
        "assistant_models": dict(models.most_common()),
        "projects": dict(projects.most_common(15)),
        "inventory": inv,
        "unused_commands": [c for c in inv["commands"] if c not in used],
        "unused_skills": [s for s in inv["skills"] if s not in used],
    }
    return metrics, prompts


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--since", required=True, help="YYYY-MM-DD, inclusive")
    parser.add_argument("--out", required=True, type=Path, help="directory for the outputs")
    args = parser.parse_args()

    since = datetime.fromisoformat(args.since).replace(tzinfo=timezone.utc)
    metrics, prompts = scan(since)
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "usage-metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    with (args.out / "usage-prompts.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["ts", "session", "project", "chars", "text"])
        writer.writeheader()
        writer.writerows(prompts)
    print(json.dumps({k: metrics[k] for k in list(metrics)[:10]}, indent=2))
    print(f"wrote {args.out / 'usage-metrics.json'} and usage-prompts.csv ({len(prompts)} rows)")


if __name__ == "__main__":
    main()
