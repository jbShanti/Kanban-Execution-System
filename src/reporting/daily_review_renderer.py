from __future__ import annotations

from src.analytics.models import ExecutionReport


def render_daily_review(report: ExecutionReport) -> str:
    """
    Render the Daily Review presentation artifact.
    
    Implements the 9-section structure from Roadmap.md Phase 2:
      1. Inbox
      2. High Five
      3. Schedule Review
      4. Board Health ✅ (fully implemented)
      5. Focus Analysis
      6. Corridor Analysis
      7. Score Suggestions
      8. Task Analysis
      9. Strategic Findings
    """
    bh = report.board_health
    
    # Безопасное извлечение статуса
    status_str = bh.status.value if hasattr(bh.status, "value") else str(bh.status)
    
    sections = [
        # ── Header ─────────────────────────────────────────────
        "# Daily Execution Report",
        "",
        f"**Analysis Date:** {report.analysis_date.isoformat()}",
        f"**Report ID:** `{report.report_id[:8]}...`",
        f"**Schema Version:** {report.schema_version}",
        "",
        
        # ── Sections 1-3: TODO (Recommendation Engine - Phase 3) ──
        "## Inbox",
        "",
        "_⚠️ Will be implemented in Phase 3 (Task Intelligence)_",
        "",
        
        "## High Five",
        "",
        "_⚠️ Will be implemented in Phase 3 (Task Intelligence)_",
        "",
        
        "## Schedule Review",
        "",
        "_⚠️ Will be implemented in Phase 3 (Task Intelligence)_",
        "",
        
        # ── Section 4: Board Health (полная реализация) ─────────
        "## Board Health",
        "",
        f"**Status:** {status_str.upper()}",
        "",
        "### Overview",
        "",
        f"- Total Tasks: **{bh.total_tasks}**",
        f"- Active Tasks: **{bh.active_tasks}**",  # ← ДОБАВИТЬ ЭТУ СТРОКУ
        f"- Completed/Archived: **{bh.total_tasks - bh.active_tasks}**",  # ← БОНУС
        f"- Missing Score: {bh.missing_score}",
        f"- Missing Tags: {bh.missing_tag}",
        f"- Orphan Tasks: {bh.orphan_tasks}",
        "",
        "### Coverage Metrics",
        "",
        f"- Score Coverage: **{bh.score_coverage:.1%}** {_coverage_bar(bh.score_coverage)}",
        f"- Tag Coverage: **{bh.tag_coverage:.1%}** {_coverage_bar(bh.tag_coverage)}",
        f"- Analytics Coverage: **{bh.analytics_coverage:.1%}** {_coverage_bar(bh.analytics_coverage)}",
        "",
    ]
    
    # ── Sample Orphans (если есть) ─────────────────────────────
    if bh.sample_orphans:
        sections.extend([
            "### ⚠️ Orphan Tasks (Top 5)",
            "",
            "_Tasks missing critical metadata (score or tags):_",
            "",
        ])
        for orphan in bh.sample_orphans[:5]:
            missing = ", ".join(m.value for m in orphan.missing)
            active_marker = "🟢" if orphan.is_active else "⚪"
            sections.append(f"- {active_marker} **{orphan.title}** — missing: `{missing}`")
        sections.append("")
    
    # ── Sections 5-8: TODO ─────────────────────────────────────
    sections.extend([
        "## Focus Analysis",
        "",
        "_⚠️ Will be implemented in Phase 2.1_",
        "",
        
        "## Corridor Analysis",
        "",
        "_⚠️ Will be implemented in Phase 2.1_",
        "",
        
        "## Score Suggestions",
        "",
        "_⚠️ Will be implemented in Phase 3 (Task Intelligence)_",
        "",
        
        "## Task Analysis",
        "",
        "_⚠️ Will be implemented in Phase 2.1_",
        "",
        
        # ── Section 9: Strategic Findings ──────────────────────
        "## Strategic Findings",
        "",
        "### Executive Summary",
        "",
        report.executive_summary.summary,
        "",
        
        # ── Footer ─────────────────────────────────────────────
        "---",
        f"*Generated at {report.generated_at.strftime('%Y-%m-%d %H:%M:%S')}*",
    ])
    
    return "\n".join(sections)


def _coverage_bar(coverage: float, width: int = 10) -> str:
    """Render a simple ASCII progress bar for coverage metrics.
    
    Examples:
        0.815 → '████████░░'
        1.0   → '██████████'
        0.5   → '█████░░░░░'
    """
    filled = int(coverage * width)
    empty = width - filled
    return "█" * filled + "░" * empty