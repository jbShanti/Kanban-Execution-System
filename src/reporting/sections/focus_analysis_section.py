from __future__ import annotations

from src.analytics.models import ExecutionReport


def render_focus_analysis_section(report: ExecutionReport) -> str:
    """
    ## Focus Analysis
    
    Анализ концентрации внимания.
    
    Включает:
    - Распределение задач по тегам
    - Топ-3 тега с наибольшим количеством задач
    - Рекомендации по фокусировке
    """
    lines: list[str] = []
    
    lines.append("## Focus Analysis")
    lines.append("")
    
    if report.board_summary is None:
        lines.append("_Board summary data not available._")
        lines.append("")
        return "\n".join(lines)
    
    # Use board summary data for focus analysis
    total_tasks = report.board_summary.total_tasks
    active_tasks = report.board_summary.active_tasks
    overdue_tasks = report.board_summary.overdue_tasks
    scored_tasks = report.board_summary.scored_tasks
    
    lines.append("### Task Distribution Overview")
    lines.append("")
    lines.append(f"- **Total Tasks:** {total_tasks}")
    lines.append(f"- **Active Tasks:** {active_tasks}")
    lines.append(f"- **Overdue Tasks:** {overdue_tasks}")
    lines.append(f"- **Scored Tasks:** {scored_tasks}/{total_tasks}")
    lines.append("")
    
    # Analyze focus by score corridors as proxy for tag distribution
    corridors = report.board_summary.score_corridors
    
    lines.append("### Focus by Priority Corridor")
    lines.append("")
    
    corridor_order = [
        ("21-25", "Critical Focus"),
        ("16-20", "High Priority"),
        ("11-15", "Medium Priority"),
        ("6-10", "Low Priority"),
        ("1-5", "Optional"),
        ("no_score", "Unscored"),
    ]
    
    has_data = False
    for corridor_key, corridor_label in corridor_order:
        corridor = corridors.get(corridor_key)
        if corridor and corridor.task_count > 0:
            has_data = True
            percentage = (corridor.task_count / total_tasks * 100) if total_tasks > 0 else 0
            bar_length = int(percentage / 5)
            bar_length = min(bar_length, 20)
            bar = "█" * bar_length + "░" * (20 - bar_length)
            lines.append(f"- **{corridor_label} ({corridor_key})**: {corridor.task_count} tasks ({percentage:.1f}%) `{bar}`")
    
    if not has_data:
        lines.append("No task distribution data available.")
        lines.append("")
        return "\n".join(lines)
    
    lines.append("")
    
    # Focus recommendations
    lines.append("### Focus Recommendations")
    lines.append("")
    
    critical_corridor = corridors.get("21-25")
    high_corridor = corridors.get("16-20")
    no_score_corridor = corridors.get("no_score")
    
    recommendations = []
    
    if critical_corridor and critical_corridor.task_count > 3:
        recommendations.append(
            f"⚠️ **Focus Dilution**: {critical_corridor.task_count} critical tasks (21-25). "
            f"Limit to 1-2 true focus tasks at a time."
        )
    elif critical_corridor and critical_corridor.task_count > 0:
        recommendations.append(
            f"✅ **Good Focus**: {critical_corridor.task_count} critical task(s) — manageable for deep work."
        )
    else:
        recommendations.append(
            "📝 **No Critical Tasks**: Consider promoting high-priority work to critical if appropriate."
        )
    
    if no_score_corridor and no_score_corridor.task_count > total_tasks * 0.3:
        recommendations.append(
            f"⚠️ **Blind Spots**: {no_score_corridor.task_count} unscored tasks ({no_score_corridor.task_count/total_tasks*100:.0f}%) — "
            f"cannot assess focus distribution accurately."
        )
    
    if overdue_tasks > 0:
        recommendations.append(
            f"🔴 **Urgent**: {overdue_tasks} overdue task(s) — resolve before starting new focus work."
        )
    
    if active_tasks > 10:
        recommendations.append(
            f"⚡ **WIP High**: {active_tasks} active tasks — apply WIP limits (3-5) to improve focus."
        )
    
    if not recommendations:
        recommendations.append("✅ Focus distribution looks healthy.")
    
    for rec in recommendations:
        lines.append(f"- {rec}")
    
    lines.append("")
    
    return "\n".join(lines)