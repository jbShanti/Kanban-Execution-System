from __future__ import annotations

from src.parser.models import Task


def render_high_five_section(
    tasks: list[Task],
) -> str:
    """Render the High Five (top 5 tasks for the day) section."""
    
    lines: list[str] = []
    
    lines.append("## High Five — Top 5 Tasks for Today")
    lines.append("")
    
    if not tasks:
        lines.append("No tasks available.")
        lines.append("")
        return "\n".join(lines)
    
    for idx, task in enumerate(tasks, start=1):
        score_str = f" (score: {task.score})" if task.score is not None else " (no score)"
        due_str = f" — due: {task.due}" if task.due else ""
        status_str = task.status.value
        
        lines.append(
            f"{idx}. **{task.title}** [{status_str}]{score_str}{due_str}"
        )
    
    lines.append("")
    
    return "\n".join(lines)