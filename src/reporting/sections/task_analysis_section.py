from __future__ import annotations

from src.analytics.models import ExecutionReport


def render_task_analysis_section(report: ExecutionReport) -> str:
    """
    ## Task Analysis
    
    Детальный анализ отдельных задач.
    
    Включает:
    - Задачи, требующие внимания (attention score высокий)
    - Задачи с рисками (overdue + high priority)
    - Задачи, готовые к выполнению (actionable)
    """
    lines: list[str] = []
    
    lines.append("## Task Analysis")
    lines.append("")
    
    if report.board_summary is None:
        lines.append("_Board summary data not available._")
        lines.append("")
        return "\n".join(lines)
    
    total_tasks = report.board_summary.total_tasks
    active_tasks = report.board_summary.active_tasks
    actionable_tasks = report.board_summary.actionable_tasks
    overdue_tasks = report.board_summary.overdue_tasks
    completed_tasks = report.board_summary.completed_tasks
    cancelled_tasks = report.board_summary.cancelled_tasks
    
    # Overview
    lines.append("### Task Status Overview")
    lines.append("")
    lines.append(f"- **Total Tasks**: {total_tasks}")
    lines.append(f"- **Active**: {active_tasks}")
    lines.append(f"- **Actionable**: {actionable_tasks}")
    lines.append(f"- **Overdue**: {overdue_tasks}")
    lines.append(f"- **Completed**: {completed_tasks}")
    lines.append(f"- **Cancelled**: {cancelled_tasks}")
    lines.append("")
    
    # Tasks requiring attention
    lines.append("### ⚠️ Tasks Requiring Attention")
    lines.append("")
    
    if overdue_tasks > 0:
        lines.append(f"- **{overdue_tasks} overdue task(s)** — Immediate action required")
    else:
        lines.append("- No overdue tasks")
    
    # High priority without due date (risk of being forgotten)
    # We can infer from score corridors
    corridors = report.board_summary.score_corridors
    critical_corridor = corridors.get("21-25")
    high_corridor = corridors.get("16-20")
    
    high_priority_count = 0
    if critical_corridor:
        high_priority_count += critical_corridor.task_count
    if high_corridor:
        high_priority_count += high_corridor.task_count
    
    if high_priority_count > 0:
        lines.append(f"- **{high_priority_count} high-priority task(s)** (score 16-25) — Ensure progress tracking")
    
    # Unscored active tasks
    no_score_corridor = corridors.get("no_score")
    if no_score_corridor and no_score_corridor.task_count > 0:
        lines.append(f"- **{no_score_corridor.task_count} unscored task(s)** — Cannot prioritize effectively")
    
    lines.append("")
    
    # Actionable tasks ready for execution
    lines.append("### ✅ Ready for Execution")
    lines.append("")
    
    if actionable_tasks > 0:
        lines.append(f"**{actionable_tasks} actionable task(s)** available for work:")
        lines.append("")
        lines.append("Recommended approach:")
        lines.append("1. Start with overdue high-priority tasks")
        lines.append("2. Continue with today's due high-priority tasks")
        lines.append("3. Pick 1-3 tasks for focused work (WIP limit)")
        lines.append("4. Defer or delegate lower priority items")
    else:
        lines.append("No actionable tasks currently. Consider:")
        lines.append("- Moving tasks from Scheduled/Queued to active sections")
        lines.append("- Breaking down larger tasks into actionable items")
        lines.append("- Reviewing Inbox for new work")
    
    lines.append("")
    
    # Risk assessment
    lines.append("### ⚠️ Risk Assessment")
    lines.append("")
    
    risks = []
    
    if overdue_tasks > 3:
        risks.append(f"High: {overdue_tasks} overdue tasks — deadline credibility at risk")
    elif overdue_tasks > 0:
        risks.append(f"Medium: {overdue_tasks} overdue task(s) — monitor closely")
    
    if high_priority_count > 10:
        risks.append(f"High: {high_priority_count} high-priority tasks — focus dilution risk")
    elif high_priority_count > 5:
        risks.append(f"Medium: {high_priority_count} high-priority tasks — prioritize ruthlessly")
    
    if no_score_corridor and no_score_corridor.task_count > total_tasks * 0.3:
        risks.append(f"Medium: {no_score_corridor.task_count} unscored tasks — prioritization blind spots")
    
    if active_tasks > 20:
        risks.append(f"High: {active_tasks} active tasks — WIP overload, context switching costs")
    elif active_tasks > 15:
        risks.append(f"Medium: {active_tasks} active tasks — approaching WIP limits")
    
    if not risks:
        risks.append("Low: No significant risks detected")
    
    for risk in risks:
        lines.append(f"- {risk}")
    
    lines.append("")
    
    return "\n".join(lines)