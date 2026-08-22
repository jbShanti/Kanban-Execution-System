"""Integration tests using a real Obsidian Kanban board.

These tests load an actual board file (either from user's vault or fixtures)
and run the full generate_execution_report → render_daily_review pipeline.
This is useful for:
  - Validating the pipeline against realistic data
  - Generating a sample report.md for review
  - Catching edge cases in real-world boards

Tests are skipped gracefully if the board file is not available.
"""

from __future__ import annotations

import os
from datetime import date
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

from src.analytics.service import generate_execution_report
from src.reporting.daily_review_renderer import render_daily_review
from tests.helper import load_test_board

if TYPE_CHECKING:
    from src.parser.models import Board


def _load_real_board() -> Board:
    """Try to load a real Kanban board from multiple locations.

    Returns the parsed board, or raises FileNotFoundError if no board
    is available (tests should skip in this case).
    """
    # 1. Environment variable (ideal for CI or other developers)
    env_path = os.getenv("KANBAN_REAL_BOARD_PATH")
    if env_path and Path(env_path).exists():
        return load_test_board(Path(env_path))

    # 2. Local developer path (raw string for Windows paths)
    local_path = Path(r"O:\Проекты\Kanban\Doing (KB).md")
    if local_path.exists():
        return load_test_board(local_path)

    # 3. Fallback to repository fixtures
    repo_path = Path("tests/fixtures/Doing (KB).md")
    if repo_path.exists():
        return load_test_board(repo_path)

    raise FileNotFoundError(
        "No Kanban board found. Set KANBAN_REAL_BOARD_PATH environment variable, "
        "place a board at O:\\Проекты\\Kanban\\, or add one to tests/fixtures/"
    )


@pytest.fixture
def real_board() -> Board:
    """Fixture that loads the real board or skips the test."""
    try:
        return _load_real_board()
    except FileNotFoundError as e:
        pytest.skip(str(e))
        raise  # Unreachable, but needed for type checker


def test_real_board_produces_execution_report(real_board: Board):
    """Real board must produce a valid ExecutionReport."""
    analysis_date = date(2026, 1, 15)

    report = generate_execution_report(real_board, analysis_date)

    # Basic contract
    assert report is not None
    assert report.schema_version == "1.0"
    assert report.analysis_date == analysis_date
    assert len(report.report_id) == 36  # UUID format

    # Board health must reflect actual content
    assert report.board_health.total_tasks > 0, (
        "Real board must contain at least one task"
    )

    # Executive summary must exist
    assert report.executive_summary is not None
    assert isinstance(report.executive_summary.summary, str)

    print("\n=== Real Board Report ===")
    print(f"Total tasks: {report.board_health.total_tasks}")
    print(f"Score coverage: {report.board_health.score_coverage:.1%}")
    print(f"Tag coverage: {report.board_health.tag_coverage:.1%}")
    print(f"Orphan tasks: {report.board_health.orphan_tasks}")
    print(f"Status: {report.board_health.status.value}")


def test_real_board_renders_daily_review(real_board: Board, tmp_path: Path):
    """Full pipeline: real board → ExecutionReport → Daily Review Markdown."""
    analysis_date = date(2026, 1, 15)

    report = generate_execution_report(real_board, analysis_date)
    markdown = render_daily_review(report)

    # Basic validation of rendered output
    assert isinstance(markdown, str)
    assert len(markdown) > 0
    assert "# Daily Execution Report" in markdown
    assert "Board Health" in markdown

    # Write to repo root for manual review (convenience for developer)
    repo_report_path = Path("report.md")
    try:
        with open(repo_report_path, "w", encoding="utf-8") as f:
            f.write(markdown)
        print(f"\nReport written to: {repo_report_path.absolute()}")
    except OSError as e:
        # May fail in CI or read-only environments — not a test failure
        print(f"\nCould not write to {repo_report_path}: {e}")

    # Also write to pytest's tmp_path (always works, auto-cleaned)
    tmp_report = tmp_path / "daily_review.md"
    tmp_report.write_text(markdown, encoding="utf-8")

    print("\n=== Rendered Daily Review (first 500 chars) ===")
    print(markdown[:500])
    print("..." if len(markdown) > 500 else "")


def test_real_board_sections_exist(real_board: Board):
    """Real board must contain at least one section."""
    sections = real_board.sections

    assert len(sections) > 0, "Real board must have at least one section"

    print("\n=== Board Sections ===")
    for section in sections:
        wip_info = f" (WIP: {section.wip_limit})" if section.wip_limit else ""
        print(f"  - {section.title} [{section.type.value}]{wip_info}")


def test_real_board_is_deterministic(real_board: Board):
    """Real board must produce identical reports on repeated invocations."""
    analysis_date = date(2026, 1, 15)

    report1 = generate_execution_report(real_board, analysis_date)
    report2 = generate_execution_report(real_board, analysis_date)

    # Metadata differs (report_id, generated_at) — expected
    assert report1.report_id != report2.report_id

    # Analytical content must be identical
    assert report1.analysis_date == report2.analysis_date
    assert report1.board_health == report2.board_health
    assert report1.executive_summary == report2.executive_summary
    assert report1.schema_version == report2.schema_version