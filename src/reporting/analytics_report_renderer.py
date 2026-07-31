from __future__ import annotations

from src.analytics.models import AnalyticsReport
from src.parser.models import Task

from src.reporting.sections.board_health_section import (
    render_board_health_section,
)
from src.reporting.sections.score_corridors_section import (
    render_score_corridors_section,
)
from src.reporting.sections.high_five_section import (
    render_high_five_section,
)


def render_analytics_report(
    report: AnalyticsReport,
) -> str:

    sections = [
        "# Analytics Report",
        "",
        render_board_health_section(
            report.board_health,
        ),
        render_score_corridors_section(
            report,
        ),
    ]

    return "\n".join(
        section
        for section in sections
        if section
    )


def render_analytics_report_with_snapshot(
    report: AnalyticsReport,
    high_five_tasks: list[Task],
) -> str:
    """Render analytics report with High Five section from snapshot."""
    
    sections = [
        "# Analytics Report",
        "",
        render_board_health_section(
            report.board_health,
        ),
        render_score_corridors_section(
            report,
        ),
        render_high_five_section(high_five_tasks),
    ]

    return "\n".join(
        section
        for section in sections
        if section
    )