from __future__ import annotations

from src.analytics.models import ExecutionReport
from src.reporting.sections.inbox_section import render_inbox_section
from src.reporting.sections.high_five_section import render_high_five_section
from src.reporting.sections.schedule_review_section import render_schedule_review_section
from src.reporting.sections.board_health_section import render_board_health_section
from src.reporting.sections.focus_analysis_section import render_focus_analysis_section
from src.reporting.sections.corridor_analysis_section import render_corridor_analysis_section
from src.reporting.sections.score_suggestions_section import render_score_suggestions_section
from src.reporting.sections.task_analysis_section import render_task_analysis_section
from src.reporting.sections.strategic_findings_section import render_strategic_findings_section


def compose_execution_report(report: ExecutionReport) -> str:
    """
    Собирает все секции в финальный Markdown отчет.
    
    Гарантирует:
    - Строгий порядок секций согласно MVP
    - Каждая секция отделена пустой строкой
    - Заголовок отчета в начале
    """
    sections = [
        "# Daily Execution Report",
        "",
        f"**Analysis Date:** {report.analysis_date.isoformat()}",
        f"**Report ID:** `{report.report_id[:8]}...`",
        f"**Schema Version:** {report.schema_version}",
        "",
        render_inbox_section(report),
        render_high_five_section(report),
        render_schedule_review_section(report),
        render_board_health_section(report),
        render_focus_analysis_section(report),
        render_corridor_analysis_section(report),
        render_score_suggestions_section(report),
        render_task_analysis_section(report),
        render_strategic_findings_section(report),
        "---",
        f"*Generated at {report.generated_at.strftime('%Y-%m-%d %H:%M:%S')}*",
    ]
    
    # Filter out empty strings and join with newlines
    # Each section already ends with a blank line
    return "\n".join(s for s in sections if s is not None)