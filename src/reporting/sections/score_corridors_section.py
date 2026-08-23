from __future__ import annotations

from src.analytics.models import ExecutionReport, ScoreCorridorSummary


def render_score_corridors_section(
    report: ExecutionReport,
) -> str:
    """Render the Score Corridors section of the Daily Review.
    
    Shows distribution of tasks across score ranges:
      - 1-5: Low priority
      - 6-10: Normal priority
      - 11-15: High priority
      - 16-20: Very high priority
      - 21-25: Focus tasks (critical)
    """
    lines: list[str] = []
    
    lines.append("## Score Corridors")
    lines.append("")
    
    if report.board_summary is None:
        lines.append("_Board summary data not available._")
        lines.append("")
        return "\n".join(lines)
    
    corridors = report.board_summary.score_corridors
    
    if not corridors:
        lines.append("No score corridor data available.")
        lines.append("")
        return "\n".join(lines)
    
    # Render each corridor
    for corridor_name, corridor in sorted(corridors.items()):
        lines.append(
            f"- **{corridor_name}**: "
            f"{corridor.task_count} tasks "
            f"({corridor.percentage_of(report.board_summary.total_tasks):.1f}%)"
        )
    
    lines.append("")
    
    # Summary metrics
    focus_tasks = _count_focus_tasks(corridors)
    high_value_tasks = _count_high_value_tasks(corridors)
    total_tasks = report.board_summary.total_tasks
    
    if total_tasks > 0:
        lines.append("### Key Metrics")
        lines.append("")
        lines.append(
            f"- **Focus Tasks (21-25)**: {focus_tasks} "
            f"({focus_tasks / total_tasks * 100:.1f}%)"
        )
        lines.append(
            f"- **High Value Tasks (16-25)**: {high_value_tasks} "
            f"({high_value_tasks / total_tasks * 100:.1f}%)"
        )
        lines.append("")
    
    return "\n".join(lines)


def _count_focus_tasks(corridors: dict[str, ScoreCorridorSummary]) -> int:
    """Count tasks in the 21-25 score range (focus tasks)."""
    return sum(
        corridor.task_count
        for name, corridor in corridors.items()
        if "21-25" in name
    )


def _count_high_value_tasks(corridors: dict[str, ScoreCorridorSummary]) -> int:
    """Count tasks in the 16-25 score range (high value tasks)."""
    return sum(
        corridor.task_count
        for name, corridor in corridors.items()
        if "16-20" in name or "21-25" in name
    )