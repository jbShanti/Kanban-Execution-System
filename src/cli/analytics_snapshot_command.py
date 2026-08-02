from __future__ import annotations

from pathlib import Path

from src.analytics.service import build_analytics_snapshot
from src.parser.parser import parse_markdown_file
from src.reporting.report_adapter import render_snapshot


def analytics_snapshot_command(
    board_path: str | Path,
) -> str:
    board_path = Path(board_path)

    board = parse_markdown_file(board_path)

    snapshot = build_analytics_snapshot(board)

    return render_snapshot(snapshot)