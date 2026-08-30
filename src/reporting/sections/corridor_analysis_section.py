from __future__ import annotations

from src.analytics.models import ExecutionReport


def render_corridor_analysis_section(report: ExecutionReport) -> str:
    """
    ## Corridor Analysis
    
    Распределение задач по скоринговым коридорам.
    
    Для каждого коридора:
    - Название коридора (critical, high, medium, low, optional)
    - Количество задач
    - Процент от общего числа
    - Процент от общего score
    
    Включает визуализацию:
    critical ████████████ 40%
    high     ████████ 25%
    ...
    """
    lines: list[str] = []
    
    lines.append("## Corridor Analysis")
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
    
    total_tasks = report.board_summary.total_tasks
    total_score = report.board_summary.total_score
    
    if total_tasks == 0:
        lines.append("No tasks to analyze.")
        lines.append("")
        return "\n".join(lines)
    
    # Define corridor order and labels
    corridor_order = [
        ("21-25", "Critical (21-25)"),
        ("16-20", "High (16-20)"),
        ("11-15", "Medium (11-15)"),
        ("6-10", "Low (6-10)"),
        ("1-5", "Optional (1-5)"),
        ("0", "Zero Score"),
        ("no_score", "No Score"),
    ]
    
    lines.append("### Task Distribution by Score Corridor")
    lines.append("")
    
    # Calculate max bar width for visualization
    max_bar_width = 20
    
    for corridor_key, corridor_label in corridor_order:
        corridor = corridors.get(corridor_key)
        if corridor is None:
            continue
            
        task_count = corridor.task_count
        if task_count == 0:
            continue
            
        percentage = (task_count / total_tasks) * 100
        score_share = (corridor.total_score / total_score * 100) if total_score > 0 else 0
        
        # Visual bar
        bar_length = int(percentage / 5)  # 20 chars = 100%
        bar_length = min(bar_length, max_bar_width)
        bar = "█" * bar_length + "░" * (max_bar_width - bar_length)
        
        lines.append(
            f"- **{corridor_label}**: {task_count} tasks "
            f"({percentage:.1f}%) | Score share: {score_share:.1f}% "
            f"`{bar}`"
        )
    
    lines.append("")
    
    # Summary metrics
    lines.append("### Summary")
    lines.append("")
    
    focus_tasks = sum(
        c.task_count for name, c in corridors.items() if "21-25" in name
    )
    high_value_tasks = sum(
        c.task_count for name, c in corridors.items() 
        if "16-20" in name or "21-25" in name
    )
    no_score_tasks = corridors.get("no_score", None)
    no_score_count = no_score_tasks.task_count if no_score_tasks else 0
    
    lines.append(f"- **Critical Focus Tasks (21-25)**: {focus_tasks} ({focus_tasks/total_tasks*100:.1f}%)")
    lines.append(f"- **High Value Tasks (16-25)**: {high_value_tasks} ({high_value_tasks/total_tasks*100:.1f}%)")
    lines.append(f"- **Tasks Without Score**: {no_score_count} ({no_score_count/total_tasks*100:.1f}%)")
    lines.append(f"- **Total Score**: {total_score}")
    lines.append(f"- **Average Score**: {total_score/total_tasks:.1f}" if total_tasks > 0 else "- **Average Score**: N/A")
    
    lines.append("")
    
    return "\n".join(lines)