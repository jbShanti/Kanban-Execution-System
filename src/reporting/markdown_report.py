from __future__ import annotations

from src.analytics.models import (
    BoardHealthReport,
    BoardMetrics,
    SectionMetrics,
)


def render_markdown_report(
    board_metrics: BoardMetrics,
    section_metrics: list[SectionMetrics],
    board_health: BoardHealthReport,
) -> str:
    lines: list[str] = []

    lines.append("# Board Health Report")
    lines.append("")

    lines.append(
        f"Health Score: "
        f"{board_health.board_health_score:.1f}/100"
    )
    lines.append("")

    lines.append("## Board Metrics")
    lines.append("")

    lines.append(
        f"- Total Tasks: "
        f"{board_metrics.total_tasks}"
    )

    lines.append(
        f"- Active Tasks: "
        f"{board_metrics.active_tasks}"
    )

    lines.append(
        f"- Actionable Tasks: "
        f"{board_metrics.actionable_tasks}"
    )

    lines.append(
        f"- Overdue Tasks: "
        f"{board_metrics.overdue_tasks}"
    )

    lines.append(
        f"- Total Score: "
        f"{board_metrics.total_score}"
    )

    lines.append("")

    lines.append("## WIP")
    lines.append("")

    lines.append(
        f"- WIP Violations: "
        f"{board_health.wip_violations}"
    )

    lines.append("")

    lines.append("## Stale")
    lines.append("")

    lines.append(
        f"- Stale Tasks: "
        f"{board_health.stale_task_count}"
    )

    lines.append("")

    lines.append("## Top Attention")
    lines.append("")

    if board_health.top_attention_tasks:
        for idx, item in enumerate(
            board_health.top_attention_tasks,
            start=1,
        ):
            lines.append(
                f"{idx}. "
                f"{item.task.title} "
                f"({item.final_score})"
            )
    else:
        lines.append("No attention items")

    lines.append("")

    lines.append("## Top Priority")
    lines.append("")

    if board_health.top_priority_tasks:
        for idx, item in enumerate(
            board_health.top_priority_tasks,
            start=1,
        ):
            lines.append(
                f"{idx}. "
                f"{item.task.title} "
                f"({item.final_score})"
            )
    else:
        lines.append("No priority items")

    lines.append("")

    lines.append("## Sections")
    lines.append("")

    if section_metrics:
        for section in section_metrics:
            lines.append(
                f"- {section.section.title}: "
                f"{section.total_tasks} tasks, "
                f"active={section.active_tasks}, "
                f"score={section.total_score}"
            )
    else:
        lines.append("No sections")

    lines.append("")

    lines.append("## Warnings")
    lines.append("")

    if board_health.warnings:
        for warning in board_health.warnings:
            lines.append(
                f"- [{warning.category}] "
                f"{warning.message}"
            )
    else:
        lines.append("No warnings")

    lines.append("")

    return "\n".join(lines)