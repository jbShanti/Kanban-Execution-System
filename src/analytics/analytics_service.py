from __future__ import annotations

from src.analytics.board_summary import build_board_summary
from src.analytics.board_metrics import build_board_metrics
from src.analytics.models import AnalyticsSnapshot
from src.analytics.section_metrics import build_section_metrics_map
from src.parser.models import Board


def build_analytics_snapshot(
    board: Board,
) -> AnalyticsSnapshot:
    """
    Build complete analytics snapshot for the board.
    """

    summary = build_board_summary(board)
    
    board_metrics = build_board_metrics(summary)

    section_metrics = build_section_metrics_map(
    board,
    summary.sections,
)

    return AnalyticsSnapshot(
        summary=summary,
        board=board_metrics,
        sections=section_metrics,
    )