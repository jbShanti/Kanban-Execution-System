from __future__ import annotations

from src.analytics.board_metrics import calculate_board_metrics
from src.analytics.models import AnalyticsSnapshot
from src.analytics.section_metrics import calculate_section_metrics
from src.parser.models import Task


def build_analytics_snapshot(
    tasks: list[Task],
) -> AnalyticsSnapshot:
    """
    Build complete analytics snapshot for the board.
    """

    board_metrics = calculate_board_metrics(tasks)
    section_metrics = calculate_section_metrics(tasks)

    return AnalyticsSnapshot(
        board=board_metrics,
        sections=section_metrics,
    )