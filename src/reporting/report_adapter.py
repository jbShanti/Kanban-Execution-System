# src/reporting/report_adapter.py

from src.analytics.models import AnalyticsSnapshot


def render_snapshot(
    snapshot: AnalyticsSnapshot,
) -> str:
    lines: list[str] = []

    lines.append("# Analytics Snapshot")
    lines.append("")

    lines.append(
        f"Total Tasks: {snapshot.summary.total_tasks}"
    )

    lines.append(
        f"Active Tasks: {snapshot.summary.active_tasks}"
    )

    lines.append(
        f"Completed Tasks: {snapshot.summary.completed_tasks}"
    )

    lines.append(
        f"Overdue Tasks: {snapshot.summary.overdue_tasks}"
    )

    lines.append(
        f"Total Score: {snapshot.summary.total_score}"
    )

    lines.append("")

    lines.append("## Sections")
    lines.append("")

    for section in snapshot.sections.values():
        lines.append(
            f"- {section.section.title}: "
            f"{section.total_tasks} tasks, "
            f"active={section.active_tasks}, "
            f"score={section.total_score}"
        )

    return "\n".join(lines)