from __future__ import annotations

from src.analytics.models import (
    BoardHealth,

)


def render_board_health_section(
    board_health: BoardHealth,
) -> str:

    lines: list[str] = []

    lines.append("## 1. Board Health")
    lines.append("")

    lines.append(
        f"- Status: {board_health.status.value.title()}"
    )

    lines.append(
        f"- Analytics Coverage: "
        f"{board_health.analytics_coverage:.1%}"
    )

    lines.append(
        f"- Score Coverage: "
        f"{board_health.score_coverage:.1%}"
    )

    lines.append(
        f"- Tag Coverage: "
        f"{board_health.tag_coverage:.1%}"
    )

    lines.append(
        f"- Orphan Tasks: "
        f"{board_health.orphan_tasks}"
    )

    lines.append(
        f"- Missing Score: "
        f"{board_health.missing_score}"
    )

    lines.append(
        f"- Missing Tags: "
        f"{board_health.missing_tag}"
    )

    lines.append("")

    if board_health.sample_orphans:

        lines.append("### Sample Orphans")
        lines.append("")

        for orphan in board_health.sample_orphans:

            missing = ", ".join(
                item.value
                for item in orphan.missing
            )

            state = (
                "Active"
                if orphan.is_active
                else "Inactive"
            )

            lines.append(
                f"- {orphan.title} "
                f"({state}; missing: {missing})"
            )

        lines.append("")

    return "\n".join(lines)