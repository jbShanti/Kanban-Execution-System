from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path

from src.parser.parser import parse_markdown_file
from src.analytics.service import generate_execution_report
from src.analytics.models import ExecutionReport
from src.reporting.execution_report_composer import compose_execution_report


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


def verify_determinism(board, analysis_date: date) -> bool:
    """Verify that the same board + date produces identical reports.
    
    Compares two consecutive runs of generate_execution_report
    to ensure business data is stable (only metadata differs).
    """
    report1: ExecutionReport = generate_execution_report(board, analysis_date)
    report2: ExecutionReport = generate_execution_report(board, analysis_date)
    
    checks: dict[str, bool] = {
        "analysis_date": report1.analysis_date == report2.analysis_date,
        "board_health": report1.board_health == report2.board_health,
        "board_summary": report1.board_summary == report2.board_summary,
        "executive_summary": report1.executive_summary == report2.executive_summary,
        "schema_version": report1.schema_version == report2.schema_version,
    }
    
    all_pass: bool = all(checks.values())
    
    print("\n🔬 Determinism Check:")
    for name, passed in checks.items():
        status = "✅" if passed else "❌"
        print(f"   {status} {name}: {'identical' if passed else 'DIFFERS!'}")
    
    # report_id SHOULD differ (it's a UUID per instance)
    id_differs: bool = report1.report_id != report2.report_id
    print(f"   {'✅' if id_differs else '❌'} report_id: {'unique per call' if id_differs else 'SAME (bug!)'}")
    
    return all_pass and id_differs


def main() -> None:
    """Generate Daily Execution Report from a Kanban board markdown file."""
    parser = argparse.ArgumentParser(description="Generate Daily Execution Report")
    parser.add_argument("--date", type=date.fromisoformat, default=None,
                        help="Analysis date (YYYY-MM-DD)")
    parser.add_argument("--output", type=Path, default=None,
                        help="Output file path (default: report.md next to board file)")
    parser.add_argument("--input", "--board", type=Path, default=None,
                        help="Path to the Kanban board markdown file (required if default board not found)")
    args = parser.parse_args()

    # ── Find and parse the board ─────────────────────────────
    if args.input is not None:
        board_path = args.input
        if not board_path.exists():
            parser.error(f"File not found: {board_path}")
    else:
        try:
            board_path = find_real_board()
        except FileNotFoundError:
            parser.error("Board file not found. Use --input to specify path.")
    
    board = parse_markdown_file(board_path)
    
    print(f"📂 Board: {board_path}")
    print(f"📋 Parsed: {len(board.tasks)} tasks in {len(board.sections)} sections")

    # ── Verify determinism ───────────────────────────────────
    analysis_date = args.date or date.today()
    if not verify_determinism(board, analysis_date):
        print("\n⚠️ Determinism issues detected!")
        return
    
    print("\n🎉 Pipeline is fully deterministic!")

    # ── Generate deterministic ExecutionReport ───────────────
    report = generate_execution_report(board, analysis_date)
    
    print(f"📊 Report ID: {report.report_id[:8]}...")
    print(f"📅 Analysis Date: {report.analysis_date}")

    # ── Render Execution Report ──────────────────────────────
    markdown = compose_execution_report(report)
    
    # ── Determine output path ────────────────────────────────
    if args.output is None:
        # Default: report.md next to the board file
        output_path = board_path.parent / "report.md"
    else:
        output_path = args.output
    
    # ── Save to file ─────────────────────────────────────────
    output_path.write_text(markdown, encoding="utf-8")
    print(f"✅ Saved to: {output_path.absolute()}")
    print(f"   Size: {len(markdown)} chars")
    print(f"   Generated at: {report.generated_at.strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    main()