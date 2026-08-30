from __future__ import annotations

from src.analytics.models import ExecutionReport


def render_board_health_section(report: ExecutionReport) -> str:
    """
    ## Board Health
    
    Общая оценка здоровья доски.
    
    Включает:
    - Health Score (0-100)
    - WIP violations
    - Stale tasks count
    - Overdue tasks count
    """
    lines: list[str] = []
    
    lines.append("## Board Health")
    lines.append("")
    
    if report.board_health is None:
        lines.append("_Board health data not available._")
        lines.append("")
        return "\n".join(lines)
    
    bh = report.board_health
    
    # Health status
    status_str = bh.status.value.title() if hasattr(bh.status, "value") else str(bh.status).title()
    lines.append(f"**Status:** {status_str}")
    lines.append("")
    
    # Health Score (0-100) - compute from coverage metrics
    health_score = int((
        bh.score_coverage * 0.4 +
        bh.tag_coverage * 0.3 +
        bh.analytics_coverage * 0.3
    ) * 100)
    lines.append(f"**Health Score:** {health_score}/100")
    lines.append("")
    
    # Coverage metrics
    lines.append("### Coverage Metrics")
    lines.append("")
    lines.append(f"- **Score Coverage:** {bh.score_coverage:.1%}")
    lines.append(f"- **Tag Coverage:** {bh.tag_coverage:.1%}")
    lines.append(f"- **Analytics Coverage:** {bh.analytics_coverage:.1%}")
    lines.append("")
    
    # Issues
    lines.append("### Issues")
    lines.append("")
    lines.append(f"- **Orphan Tasks:** {bh.orphan_tasks}")
    lines.append(f"- **Missing Score:** {bh.missing_score}")
    lines.append(f"- **Missing Tags:** {bh.missing_tag}")
    lines.append(f"- **Overdue Tasks:** {report.board_summary.overdue_tasks if report.board_summary else 'N/A'}")
    lines.append("")
    
    # WIP violations - note: SectionSummary doesn't have wip_limit
    # This would need SectionMetrics from analytics service
    lines.append("- **WIP Violations:** See detailed analytics for section-level WIP status")
    lines.append("")
    
    # Sample orphans
    if bh.sample_orphans:
        lines.append("### Sample Orphan Tasks (Top 5)")
        lines.append("")
        lines.append("_Tasks missing critical metadata (score or tags):_")
        lines.append("")
        for orphan in bh.sample_orphans[:5]:
            missing = ", ".join(item.value for item in orphan.missing)
            active_marker = "🟢" if orphan.is_active else "⚪"
            lines.append(f"- {active_marker} **{orphan.title}** — missing: `{missing}`")
        lines.append("")
    
    return "\n".join(lines)