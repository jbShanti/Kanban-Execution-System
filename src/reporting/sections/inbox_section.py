from __future__ import annotations

from src.analytics.models import ExecutionReport


def render_inbox_section(report: ExecutionReport) -> str:
    """
    ## Inbox
    
    Показывает задачи в статусе Inbox, требующие обработки.
    
    Если inbox пуст:
    "✅ Inbox is clear. No unprocessed tasks."
    
    Если есть задачи:
    Список задач с метаданными (title, tags, due_date если есть)
    """
    lines: list[str] = []
    
    lines.append("## Inbox")
    lines.append("")
    
    if report.board_summary is None:
        lines.append("_Board summary data not available._")
        lines.append("")
        return "\n".join(lines)
    
    # Get inbox tasks from board summary sections
    inbox_section = report.board_summary.sections.get("Inbox")
    if inbox_section is None:
        # Try case-insensitive search
        inbox_section = next(
            (s for name, s in report.board_summary.sections.items() 
             if name.lower() == "inbox"), 
            None
        )
    
    if inbox_section is None or inbox_section.total_tasks == 0:
        lines.append("✅ Inbox is clear. No unprocessed tasks.")
        lines.append("")
        return "\n".join(lines)
    
    # We need to get actual tasks from the board to show details
    # For now, show summary info
    lines.append(f"📥 **{inbox_section.total_tasks} unprocessed task(s) in Inbox**")
    lines.append("")
    lines.append(f"- Active: {inbox_section.active_tasks}")
    lines.append(f"- Actionable: {inbox_section.actionable_tasks}")
    lines.append(f"- Scored: {inbox_section.scored_tasks}/{inbox_section.total_tasks}")
    if inbox_section.scored_tasks > 0:
        lines.append(f"- Average Score: {inbox_section.average_score:.1f}")
    lines.append("")
    
    return "\n".join(lines)