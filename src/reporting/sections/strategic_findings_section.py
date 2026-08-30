from __future__ import annotations

from src.analytics.models import ExecutionReport


def render_strategic_findings_section(report: ExecutionReport) -> str:
    """
    ## Strategic Findings
    
    Стратегические выводы и рекомендации.
    
    Включает:
    - Executive Summary (краткое резюме)
    - Главные риски
    - Главные возможности
    - Рекомендуемые действия на сегодня
    """
    lines: list[str] = []
    
    lines.append("## Strategic Findings")
    lines.append("")
    
    if report.board_summary is None:
        lines.append("_Board summary data not available._")
        lines.append("")
        return "\n".join(lines)
    
    # Executive Summary
    lines.append("### Executive Summary")
    lines.append("")
    
    if report.executive_summary and report.executive_summary.summary:
        lines.append(report.executive_summary.summary)
    else:
        # Generate a basic summary from available data
        total = report.board_summary.total_tasks
        active = report.board_summary.active_tasks
        overdue = report.board_summary.overdue_tasks
        health_status = report.board_health.status.value if report.board_health else "unknown"
        
        lines.append(
            f"Board contains **{total} total tasks** with **{active} active**. "
            f"Health status: **{health_status.title()}**. "
            f"{f'**{overdue} overdue tasks** require immediate attention.' if overdue > 0 else 'No overdue tasks.'}"
        )
    
    lines.append("")
    
    # Key Risks
    lines.append("### 🔴 Key Risks")
    lines.append("")
    
    risks = []
    
    if report.board_summary.overdue_tasks > 0:
        risks.append(f"**Overdue Work**: {report.board_summary.overdue_tasks} task(s) past due — impacts credibility and flow")
    
    if report.board_summary.active_tasks > 15:
        risks.append(f"**WIP Overload**: {report.board_summary.active_tasks} active tasks — exceeds cognitive capacity, increases context switching")
    
    if report.board_health and report.board_health.missing_score > report.board_summary.total_tasks * 0.2:
        risks.append(f"**Scoring Gaps**: {report.board_health.missing_score} tasks without scores — prioritization is guesswork")
    
    if report.board_health and report.board_health.orphan_tasks > 5:
        risks.append(f"**Orphan Tasks**: {report.board_health.orphan_tasks} tasks missing critical metadata — invisible to planning")
    
    if report.board_health and report.board_health.score_coverage < 0.8:
        risks.append(f"**Low Score Coverage**: {report.board_health.score_coverage:.0%} — corridor analysis unreliable")
    
    if not risks:
        risks.append("No critical risks identified at this time.")
    
    for risk in risks:
        lines.append(f"- {risk}")
    
    lines.append("")
    
    # Key Opportunities
    lines.append("### 🟢 Key Opportunities")
    lines.append("")
    
    opportunities = []
    
    corridors = report.board_summary.score_corridors
    critical_corridor = corridors.get("21-25")
    high_corridor = corridors.get("16-20")
    
    high_value_count = 0
    if critical_corridor:
        high_value_count += critical_corridor.task_count
    if high_corridor:
        high_value_count += high_corridor.task_count
    
    if high_value_count > 0:
        opportunities.append(f"**High-Value Portfolio**: {high_value_count} tasks scored 16-25 — focus here for maximum impact")
    
    if report.board_summary.actionable_tasks > 0 and report.board_summary.active_tasks < 10:
        opportunities.append(f"**Execution Capacity**: {report.board_summary.actionable_tasks} actionable tasks with room for more — good throughput potential")
    
    if report.board_health and report.board_health.score_coverage > 0.9:
        opportunities.append("**High Data Quality**: Excellent score coverage enables reliable analytics and automation")
    
    if report.board_health and report.board_health.orphan_tasks == 0:
        opportunities.append("**Clean Board**: No orphan tasks — all work is visible and trackable")
    
    completed = report.board_summary.completed_tasks
    if completed > 0:
        opportunities.append(f"**Momentum**: {completed} completed tasks — leverage completion energy for next cycle")
    
    if not opportunities:
        opportunities.append("No standout opportunities — focus on stabilizing current workflow.")
    
    for opp in opportunities:
        lines.append(f"- {opp}")
    
    lines.append("")
    
    # Recommended Actions for Today
    lines.append("### 🎯 Recommended Actions for Today")
    lines.append("")
    
    actions = []
    
    # Priority 1: Overdue
    if report.board_summary.overdue_tasks > 0:
        actions.append(f"1. **Clear overdue**: Address {report.board_summary.overdue_tasks} overdue task(s) immediately")
    
    # Priority 2: High priority actionable
    if high_value_count > 0:
        actions.append(f"2. **Advance high-value work**: Make progress on top 3 priority tasks (score 16-25)")
    
    # Priority 3: Scoring gaps
    if report.board_health and report.board_health.missing_score > 0:
        actions.append(f"3. **Score unscored tasks**: Add scores to {report.board_health.missing_score} task(s) to enable prioritization")
    
    # Priority 4: WIP management
    if report.board_summary.active_tasks > 10:
        actions.append(f"4. **Reduce WIP**: Move {report.board_summary.active_tasks - 5} tasks to Scheduled/Queued to respect WIP limits")
    
    # Priority 5: Orphans
    if report.board_health and report.board_health.orphan_tasks > 0:
        actions.append(f"5. **Fix orphans**: Add missing metadata to {report.board_health.orphan_tasks} orphan task(s)")
    
    if not actions:
        actions.append("1. **Maintain current pace** — Board is healthy, continue steady execution")
        actions.append("2. **Weekly review** — Schedule time to reassess priorities and scores")
    
    for action in actions:
        lines.append(f"- {action}")
    
    lines.append("")
    
    return "\n".join(lines)