"""Claude Trends driver.

    python run.py                          # usage metrics (last 30 days) then render
    python run.py --usage --since 2026-10-12   # measure usage into data/usage/
    python run.py --render                 # docs/index.html and local/usage.html

Render reads the latest ``data/runs/*.json`` for the public page and the latest
``data/usage/`` for the local page. The public page never reads ``data/usage/``.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from claude_trends import render  # noqa: E402


def run_usage(since: str) -> None:
    out = ROOT / "data" / "usage"
    subprocess.run(
        [sys.executable, "-m", "claude_trends.usage", "--since", since, "--out", str(out)],
        cwd=ROOT,
        check=True,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--usage", action="store_true", help="measure usage into data/usage/")
    parser.add_argument("--since", help="YYYY-MM-DD for --usage (default: 30 days ago)")
    parser.add_argument("--render", action="store_true", help="render both pages")
    args = parser.parse_args()

    do_usage = args.usage or not (args.usage or args.render)
    do_render = args.render or not (args.usage or args.render)

    if do_usage:
        run_usage(args.since or (date.today() - timedelta(days=30)).isoformat())
    if do_render:
        for path in render.build(ROOT):
            print(f"wrote {path}")


if __name__ == "__main__":
    main()
