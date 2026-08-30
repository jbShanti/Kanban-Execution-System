from __future__ import annotations

from src.analytics.models import ExecutionReport


def render_score_suggestions_section(report: ExecutionReport) -> str:
    """
    ## Score Suggestions
    
    Рекомендации по корректировке scores.
    
    Включает:
    - Задачи с подозрительно низким score (возможно недооценены)
    - Задачи с подозрительно высоким score (возможно переоценены)
    - Задачи без score, требующие оценки
    """
    lines: list[str] = []
    
    lines.append("## Score Suggestions")
    lines.append("")
    
    if report.board_summary is None:
        lines.append("_Board summary data not available._")
        lines.append("")
        return "\n".join(lines)
    
    total_tasks = report.board_summary.total_tasks
    unscored_tasks = report.board_summary.unscored_tasks
    scored_tasks = report.board_summary.scored_tasks
    total_score = report.board_summary.total_score
    avg_score = total_score / scored_tasks if scored_tasks > 0 else 0
    
    # Tasks without score
    lines.append("### Tasks Requiring Score")
    lines.append("")
    
    if unscored_tasks > 0:
        lines.append(f"⚠️ **{unscored_tasks} task(s) without score** ({unscored_tasks/total_tasks*100:.1f}% of total)")
        lines.append("")
        lines.append("These tasks need priority assessment:")
        lines.append("- Add score metadata to enable proper prioritization")
        lines.append("- Consider using scoring guidelines: 1-5 (low), 6-10 (normal), 11-15 (high), 16-20 (very high), 21-25 (critical)")
    else:
        lines.append("✅ All tasks have scores assigned.")
    
    lines.append("")
    
    # Score distribution analysis
    lines.append("### Score Distribution Analysis")
    lines.append("")
    
    corridors = report.board_summary.score_corridors
    
    # Check for potential issues
    no_score_corridor = corridors.get("no_score")
    zero_score_corridor = corridors.get("0")
    low_score_corridor = corridors.get("1-5")
    critical_corridor = corridors.get("21-25")
    
    issues_found = False
    
    if no_score_corridor and no_score_corridor.task_count > 0:
        lines.append(f"- **No Score**: {no_score_corridor.task_count} tasks lack scores — cannot be prioritized effectively")
        issues_found = True
    
    if zero_score_corridor and zero_score_corridor.task_count > 0:
        lines.append(f"- **Zero Score**: {zero_score_corridor.task_count} tasks have score=0 — verify if intentional")
        issues_found = True
    
    if low_score_corridor and low_score_corridor.task_count > total_tasks * 0.5:
        lines.append(f"- **Low Score Concentration**: {low_score_corridor.task_count} tasks in 1-5 range — may indicate under-scoring")
        issues_found = True
    
    if critical_corridor and critical_corridor.task_count > total_tasks * 0.3:
        lines.append(f"- **Critical Overload**: {critical_corridor.task_count} tasks in 21-25 range — verify if all are truly critical")
        issues_found = True
    
    if not issues_found:
        lines.append("No obvious scoring anomalies detected.")
    
    lines.append("")
    
    # Recommendations
    lines.append("### Recommendations")
    lines.append("")
    
    if unscored_tasks > 0:
        lines.append("1. **Score unscored tasks** — Add scores to enable corridor analysis and prioritization")
    
    if zero_score_corridor and zero_score_corridor.task_count > 0:
        lines.append("2. **Review zero-score tasks** — Confirm if score=0 is intentional or if tasks need re-evaluation")
    
    if avg_score > 0:
        lines.append(f"3. **Calibrate around average** — Current average score: {avg_score:.1f}. Tasks significantly above/below may need review")
    
    lines.append("4. **Regular scoring review** — Re-assess scores during weekly reviews to maintain accuracy")
    
    lines.append("")
    
    return "\n".join(lines)