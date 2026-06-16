from __future__ import annotations

from src.analytics.models import AnalyticsReport


def render_score_corridors_section(
    report: AnalyticsReport,
) -> str:

    lines: list[str] = []

    lines.append("## 2. Score Corridors")
    lines.append("")

    if not report.corridors:
        lines.append("No score corridor data available.")
        lines.append("")

        return "\n".join(lines)

    for corridor in report.corridors:

        lines.append(
            f"- {corridor.name}: "
            f"{corridor.task_count} tasks "
            f"({corridor.percentage:.1f}%)"
        )

    lines.append("")

    lines.append(
        f"- Focus Tasks (21-25): "
        f"{report.focus_tasks} "
        f"({report.focus_percentage:.1f}%)"
    )

    lines.append(
        f"- High Value Tasks (16-25): "
        f"{report.high_value_tasks} "
        f"({report.high_value_percentage:.1f}%)"
    )

    lines.append("")

    return "\n".join(lines)