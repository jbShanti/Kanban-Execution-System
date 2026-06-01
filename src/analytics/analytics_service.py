from __future__ import annotations

from src.analytics.board_summary import build_board_summary
from src.analytics.board_metrics import calculate_board_metrics
from src.analytics.models import AnalyticsSnapshot##, AnalyticsContext
from src.analytics.section_metrics import calculate_section_metrics
from src.parser.models import Board


def build_analytics_snapshot(
    board: Board,
) -> AnalyticsSnapshot:
    """
    Build complete analytics snapshot for the board.
    """

    summary = build_board_summary(board)
    
    """ context = AnalyticsContext(
        board=board,
        summary=summary,
    )
 """
    board_metrics = calculate_board_metrics(board)

    section_metrics = calculate_section_metrics(board)

    return AnalyticsSnapshot(
        summary=summary,
        board=board_metrics,
        sections=section_metrics,
    )