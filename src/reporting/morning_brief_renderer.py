"""Generate a deterministic Morning Brief from the real board.

Usage:
    python morning_brief.py
    python morning_brief.py --date 2026-01-15
    python morning_brief.py --output brief.md --date 2026-01-15
"""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path

from src.parser.parser import parse_markdown_file
from src.analytics.service import generate_execution_report
from src.reporting.daily_review_renderer import render_daily_review


def find_real_board() -> Path:
    """Find the real board file."""
    candidates = [
        Path(r"O:\Проекты\Kanban\Doing (KB).md"),
        Path("tests/fixtures/Doing (KB).md"),
        Path("board.md"),
    ]
    
    for path in candidates:
        if path.exists():
            return path
    
    raise FileNotFoundError(
        "Real board not found. Place it at O:\\Проекты\\Kanban\\ "
        "or tests/fixtures/"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate Morning Brief")
    parser.add_argument("--date", type=date.fromisoformat, default=None,
                        help="Analysis date (YYYY-MM-DD)")
    parser.add_argument("--output", type=Path, default=Path("morning_brief.md"),
                        help="Output file path")
    args = parser.parse_args()

    # ── Find and parse the board ─────────────────────────────
    board_path = find_real_board()
    board = parse_markdown_file(board_path)
    
    print(f"📂 Board: {board_path}")
    print(f"📋 Parsed: {len(board.tasks)} tasks in {len(board.sections)} sections")

    # ── Generate deterministic ExecutionReport ───────────────
    report = generate_execution_report(board, args.date)
    
    print(f"📊 Report ID: {report.report_id[:8]}...")
    print(f"📅 Analysis Date: {report.analysis_date}")

    # ── Render Morning Brief ─────────────────────────────────
    markdown = render_daily_review(report)
    
    # ── Save to file ─────────────────────────────────────────
    args.output.write_text(markdown, encoding="utf-8")
    print(f"✅ Saved to: {args.output.absolute()}")
    print(f"   Size: {len(markdown)} chars")


if __name__ == "__main__":
    main()
    
    
def verify_determinism(board, analysis_date: date) -> bool:
    """Verify that the same board + date produces identical reports."""
    report1 = generate_execution_report(board, analysis_date)
    report2 = generate_execution_report(board, analysis_date)
    
    checks = {
        "analysis_date": report1.analysis_date == report2.analysis_date,
        "board_health": report1.board_health == report2.board_health,
        "board_summary": report1.board_summary == report2.board_summary,
        "executive_summary": report1.executive_summary == report2.executive_summary,
        "schema_version": report1.schema_version == report2.schema_version,
    }
    
    all_pass = all(checks.values())
    
    print("\n🔬 Determinism Check:")
    for name, passed in checks.items():
        status = "✅" if passed else "❌"
        print(f"   {status} {name}: {'identical' if passed else 'DIFFERS!'}")
    
    # report_id SHOULD differ (it's a UUID per instance)
    id_differs = report1.report_id != report2.report_id
    print(f"   {'✅' if id_differs else '❌'} report_id: {'unique per call' if id_differs else 'SAME (bug!)'}")
    
    return all_pass and id_differs