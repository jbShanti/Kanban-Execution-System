from __future__ import annotations

from pathlib import Path
from datetime import date

from src.analytics.service import generate_execution_report
from src.parser.parser import parse_markdown_file
from src.reporting.daily_review_renderer import render_daily_review


def analytics_snapshot_command(
    board_path: str | Path,
    analysis_date: date | None = None,
) -> str:
    """
    CLI command to generate daily execution report.
    
    Args:
        board_path: Path to the Obsidian Markdown board
        analysis_date: Optional date for analysis (defaults to today)
    
    Returns:
        Markdown report as string
    """
    board_path = Path(board_path)
    board = parse_markdown_file(board_path)
    
    # ✅ Используем новую функцию
    report = generate_execution_report(board, analysis_date)
    
    # ✅ Используем новый рендерер
    return render_daily_review(report)