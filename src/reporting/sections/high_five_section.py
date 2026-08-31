from __future__ import annotations

from src.analytics.models import ExecutionReport


def render_high_five_section(report: ExecutionReport) -> str:
    """
    ## High Five
    
    Топ-5 задач на сегодня, отсортированные по приоритету.
    
    Формат для каждой задачи:
    ### {index}. {title}
    - **Score:** {score}
    - **Due:** {due_date} или "No due date"
    - **Project:** {project} или "No project"
    
    Если меньше 5 задач:
    "⚠️ Only {count} tasks available for High Five."
    """
    lines: list[str] = []
    
    lines.append("## High Five")
    lines.append("")
    
    if report.board_summary is None:
        lines.append("_Board summary data not available._")
        lines.append("")
        return "\n".join(lines)
    
    # Get actionable tasks from board summary sections
    # We need to find the top 5 tasks by score
    # For now, use the sections data to estimate
    actionable_tasks = report.board_summary.actionable_tasks
    # total_tasks = report.board_summary.total_tasks
    
    if actionable_tasks == 0:
        lines.append("⚠️ Only 0 tasks available for High Five.")
        lines.append("")
        return "\n".join(lines)
    
    # Since we don't have individual tasks in ExecutionReport,
    # we'll show a summary based on available data
    # In a full implementation, this would come from a task snapshot
    lines.append(f"📋 **{min(actionable_tasks, 5)} of {actionable_tasks} actionable tasks highlighted**")
    lines.append("")
    
    if actionable_tasks < 5:
        lines.append(f"⚠️ Only {actionable_tasks} tasks available for High Five.")
        lines.append("")
    
    # Show corridor info as proxy for top tasks
    corridors = report.board_summary.score_corridors
    # critical_corridor = corridors.get("21-25")
    # medium_corridor = corridors.get("21-25")
    # high_corridor = corridors.get("16-20")
    
    count = 0
    for corridor_key, corridor_label in [
        ("21-25", "Critical"),
        ("16-20", "High"),
        ("11-15", "Medium"),
    ]:
        corridor = corridors.get(corridor_key)
        if corridor and corridor.task_count > 0 and count < 5:
            remaining = min(corridor.task_count, 5 - count)
            lines.append(f"### {count + 1}. {corridor_label} Priority Tasks ({remaining})")
            lines.append(f"- **Score Range:** {corridor_key}")
            lines.append(f"- **Count:** {corridor.task_count}")
            lines.append(f"- **Avg Score:** {corridor.average_score:.1f}")
            lines.append(f"- **Due:** See Schedule Review")
            lines.append(f"- **Project:** See Task Analysis")
            lines.append("")
            count += remaining
    
    if count == 0:
        lines.append("No scored actionable tasks found. Score your tasks to enable High Five.")
        lines.append("")
    
    return "\n".join(lines)