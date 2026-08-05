from __future__ import annotations

from pathlib import Path
from datetime import date, datetime, timezone

from src.analytics.service import build_analytics_snapshot
from src.parser.parser import parse_markdown_file
from src.reporting.report_adapter import render_snapshot


def analytics_snapshot_command(
    board_path: str | Path,
    analysis_date: date | None = None,
) -> str:
    board_path = Path(board_path)

    board = parse_markdown_file(board_path)

    if analysis_date is None:
        analysis_date = datetime.now(timezone.utc).date()

    snapshot = build_analytics_snapshot(board, analysis_date)

    return render_snapshot(snapshot)