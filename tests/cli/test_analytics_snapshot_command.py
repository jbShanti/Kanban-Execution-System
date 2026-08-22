"""Tests for analytics_snapshot_command CLI command.

These tests verify the end-to-end CLI pipeline:
  board.md → analytics_snapshot_command → Daily Execution Report (Markdown)
"""

from __future__ import annotations

from datetime import date
from pathlib import Path

from src.cli.analytics_snapshot_command import analytics_snapshot_command


def test_analytics_snapshot_command_generates_report(tmp_path: Path):
    """CLI command must produce a valid Daily Execution Report."""
    board = tmp_path / "board.md"
    board.write_text(
        """
# Doing

- [ ] Important task [score::20]
- [ ] Another task [score::10]
""",
        encoding="utf-8",
    )

    report = analytics_snapshot_command(board)

    # --- Basic contract ---
    assert isinstance(report, str)
    assert len(report) > 0

    # --- New report structure (post-migration) ---
    assert "# Daily Execution Report" in report
    assert "**Analysis Date:**" in report
    assert "## Board Health" in report
    assert "## Executive Summary" in report

    # --- Board content must be reflected ---
    assert "Total Tasks" in report
    assert "Status" in report


def test_analytics_snapshot_command_handles_empty_board(tmp_path: Path):
    """CLI command must handle an empty board gracefully."""
    board = tmp_path / "empty_board.md"
    board.write_text(
        """
# Doing

""",
        encoding="utf-8",
    )

    report = analytics_snapshot_command(board)

    # Must still produce a valid report (not crash)
    assert isinstance(report, str)
    assert "# Daily Execution Report" in report
    assert "## Board Health" in report

    # Empty board has 0 tasks
    assert "Total Tasks" in report


def test_analytics_snapshot_command_with_explicit_date(tmp_path: Path):
    """CLI command must use injected analysis_date instead of today."""
    board = tmp_path / "board.md"
    board.write_text(
        """
# Doing

- [ ] Task [score::15]
""",
        encoding="utf-8",
    )

    target_date = date(2026, 3, 15)
    report = analytics_snapshot_command(board, analysis_date=target_date)

    # Injected date must appear in the report
    assert "2026-03-15" in report


def test_analytics_snapshot_command_default_date_is_today(tmp_path: Path):
    """CLI command must use today's date when analysis_date is not provided."""
    board = tmp_path / "board.md"
    board.write_text(
        """
# Doing

- [ ] Task [score::10]
""",
        encoding="utf-8",
    )

    report = analytics_snapshot_command(board)

    # Today's date must appear in the report
    today_iso = date.today().isoformat()
    assert today_iso in report