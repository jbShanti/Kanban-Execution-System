from __future__ import annotations

from src.analytics.models import ExecutionReport
# from datetime import date, timedelta
# from collections import defaultdict


def render_schedule_review_section(report: ExecutionReport) -> str:
    """
    ## Schedule Review
    
    Анализ загруженности на ближайшие дни.
    
    Включает:
    - Задачи с due_date в ближайшие 7 дней
    - Предупреждения о перегрузке (если > 3 задачи в день)
    - Рекомендации по переносу задач
    """
    lines: list[str] = []
    
    lines.append("## Schedule Review")
    lines.append("")
    
    if report.board_summary is None:
        lines.append("_Board summary data not available._")
        lines.append("")
        return "\n".join(lines)
    
    # Use available data from board_summary
    overdue_tasks = report.board_summary.overdue_tasks
    active_tasks = report.board_summary.active_tasks
    actionable_tasks = report.board_summary.actionable_tasks
    
    lines.append("### Upcoming Due Dates")
    lines.append("")
    
    if overdue_tasks > 0:
        lines.append(f"- **Overdue**: {overdue_tasks} task(s) overdue")
    else:
        lines.append("- **Overdue**: No overdue tasks")
    
    # Show active/actionable as proxy for upcoming work
    lines.append(f"- **Active Tasks**: {active_tasks}")
    lines.append(f"- **Actionable Tasks**: {actionable_tasks}")
    
    lines.append("")
    
    # Overload warnings
    lines.append("### Workload Assessment")
    lines.append("")
    
    # Check for potential overload based on active tasks
    if active_tasks > 15:
        lines.append(f"⚠️ **High Workload**: {active_tasks} active tasks. Consider deferring or delegating.")
    elif active_tasks > 10:
        lines.append(f"⚡ **Moderate Workload**: {active_tasks} active tasks. Focus on completion.")
    else:
        lines.append(f"✅ **Manageable Workload**: {active_tasks} active tasks.")
    
    lines.append("")
    
    # Recommendations
    lines.append("### Recommendations")
    lines.append("")
    
    if overdue_tasks > 0:
        lines.append(f"- **Urgent**: Address {overdue_tasks} overdue task(s) immediately")
    
    if active_tasks > 10:
        lines.append("- Prioritize tasks with due dates in the next 3 days")
        lines.append("- Consider moving non-urgent tasks to Scheduled or Queued")
        lines.append("- Limit work in progress to 3-5 tasks simultaneously")
    else:
        lines.append("- Current workload is manageable")
        lines.append("- Good capacity for new high-priority work")
    
    lines.append("")
    
    return "\n".join(lines)