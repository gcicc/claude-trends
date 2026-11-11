"""Tests: _embed escaping, the usage parser on a synthetic transcript, the privacy split."""

from __future__ import annotations

import csv
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

from claude_trends import render, usage

ROOT = Path(__file__).resolve().parents[1]
SECRET = "ZXQ-SECRET-PROMPT-7731 renew the lease on the cabin"


# ---------- _embed -----------------------------------------------------------


def test_embed_escapes_script_close_and_comment_open():
    data = {"t": "a </script><script>alert(1)</script> <!-- x"}
    text = render._embed(data)
    assert "</script>" not in text
    assert "<!--" not in text
    assert "</" not in text


def test_embed_round_trips_through_json_unescape():
    data = {"t": "x </script> y <!-- z", "n": [1, 2]}
    # The browser sees the JSON string after HTML parsing: only "<\/" -> "</" at the
    # JS level, so json.loads of the text must give back the original value.
    assert (
        json.loads(render._embed(data).replace("\\u003c!--", "<!--").replace("<\\/", "</")) == data
    )


# ---------- usage parser -----------------------------------------------------


def _record(kind: str, content, ts: str, **extra) -> dict:
    base = {
        "type": kind,
        "timestamp": ts,
        "sessionId": "sess-0001-abcdef",
        "cwd": "C:\\Users\\someone\\Dropbox\\proj",
        "message": {"role": kind, "content": content},
    }
    base.update(extra)
    return base


def _write_fixture(tmp_path: Path) -> Path:
    projects = tmp_path / "projects" / "proj"
    projects.mkdir(parents=True)
    rows = [
        # a human prompt (11 chars)
        _record("user", "hello there", "2026-10-20T10:00:00Z"),
        # a slash command typed: harness-formatted, so it is not a prompt
        _record(
            "user",
            "<command-name>/trends</command-name><command-args></command-args>",
            "2026-10-20T10:01:00Z",
        ),
        # Claude invokes a skill and proposes a plan
        _record(
            "assistant",
            [
                {"type": "tool_use", "id": "t1", "name": "Skill", "input": {"skill": "dataviz"}},
                {"type": "tool_use", "id": "t2", "name": "ExitPlanMode", "input": {}},
            ],
            "2026-10-20T10:02:00Z",
        ),
        # the plan is rejected
        _record(
            "user",
            [
                {"type": "tool_result", "tool_use_id": "t1", "content": "ok"},
                {
                    "type": "tool_result",
                    "tool_use_id": "t2",
                    "content": "The user doesn't want to proceed with this tool use.",
                },
            ],
            "2026-10-20T10:03:00Z",
        ),
        # an interruption
        _record("user", "[Request interrupted by user]", "2026-10-20T10:04:00Z"),
        # a second human prompt (30 chars)
        _record("user", "x" * 30, "2026-10-20T10:05:00Z"),
        # a subagent record that must be ignored
        _record("user", "sidechain text", "2026-10-20T10:06:00Z", isSidechain=True),
        # before the window: ignored
        _record("user", "ancient prompt", "2026-09-01T10:00:00Z"),
    ]
    (projects / "s1.jsonl").write_text(
        "\n".join(json.dumps(r) for r in rows) + "\nnot json\n", encoding="utf-8"
    )
    return tmp_path


def test_usage_scan_exact_counts(tmp_path, monkeypatch):
    base = _write_fixture(tmp_path)
    monkeypatch.setattr(usage, "TRANSCRIPTS", base / "projects")
    monkeypatch.setattr(usage, "CLAUDE", base)
    since = datetime(2026, 10, 1, tzinfo=timezone.utc)
    metrics, prompts = usage.scan(since)

    assert metrics["prompts"] == 2
    assert metrics["sessions"] == 1
    assert metrics["interruptions"] == 1
    assert metrics["slash_commands"] == {"trends": 1}
    assert metrics["skills_invoked_by_claude"] == {"dataviz": 1}
    assert metrics["tools"] == {"Skill": 1, "ExitPlanMode": 1}
    assert metrics["tool_rejections"] == {"ExitPlanMode": {"rejected": 1, "calls": 1}}
    assert metrics["prompt_chars_median"] == 20.5
    assert metrics["prompt_share_under_60"] == 1.0
    assert [p["chars"] for p in prompts] == [11, 30]
    assert metrics["projects"] == {"C:/Users/someone/Dropbox/proj": 2}


# ---------- render: privacy split --------------------------------------------


def test_public_page_contains_nothing_from_usage(tmp_path, monkeypatch):
    root = tmp_path / "site"
    (root / "data" / "runs").mkdir(parents=True)
    (root / "data" / "usage").mkdir(parents=True)
    (root / "reports").mkdir()
    shutil.copy(ROOT / "data" / "runs" / "2026-10-29.json", root / "data" / "runs")
    shutil.copy(ROOT / "reports" / "claude-trends-index.md", root / "reports")

    base = _write_fixture(tmp_path / "t")
    monkeypatch.setattr(usage, "TRANSCRIPTS", base / "projects")
    monkeypatch.setattr(usage, "CLAUDE", base)
    metrics, _ = usage.scan(datetime(2026, 10, 1, tzinfo=timezone.utc))
    (root / "data" / "usage" / "usage-metrics.json").write_text(
        json.dumps(metrics), encoding="utf-8"
    )
    with (root / "data" / "usage" / "usage-prompts.csv").open(
        "w", newline="", encoding="utf-8"
    ) as fh:
        writer = csv.DictWriter(fh, fieldnames=["ts", "session", "project", "chars", "text"])
        writer.writeheader()
        writer.writerow(
            {"ts": "t", "session": "s", "project": "p", "chars": len(SECRET), "text": SECRET}
        )
    (root / "data" / "usage" / "coaching.json").write_text(
        json.dumps({"adoption_gap": [{"text": SECRET, "evidence_count": 3, "action": "x"}]}),
        encoding="utf-8",
    )

    written = {p.name for p in render.build(root)}
    assert written == {"index.html", "usage.html"}

    public = (root / "docs" / "index.html").read_text(encoding="utf-8")
    local = (root / "local" / "usage.html").read_text(encoding="utf-8")
    assert "ZXQ-SECRET" not in public
    assert "usage.html" not in public
    assert 'data-section="claude-trends"' in public
    assert "2026-10-29" in public
    # the local page does use its own data (coaching), proving the fixture is live
    assert "ZXQ-SECRET" in local
    assert 'data-section="claude-trends"' in local


def test_index_parser_marks_legacy_and_sorts():
    rows = render.load_index(ROOT / "reports" / "claude-trends-index.md")
    dates = [r["date"] for r in rows]
    assert dates == sorted(dates, reverse=True)
    assert any(r["legacy"] for r in rows)
    assert rows[0]["href"] == "../reports/claude-trends-2026-10-29-delta.md"
