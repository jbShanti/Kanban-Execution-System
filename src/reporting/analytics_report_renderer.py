from __future__ import annotations

from src.analytics.models import AnalyticsReport

from src.reporting.sections.board_health_section import (
    render_board_health_section,
)
from src.reporting.sections.score_corridors_section import (
    render_score_corridors_section,
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