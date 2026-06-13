from src.analytics.models import (
    AttentionScore,
    BoardHealthReport,
    HealthWarning,
    PriorityScore,
    SectionSummary,
    OverloadSignal
)
from src.analytics.models import (
    BoardMetrics,
    SectionMetrics,
)
from src.parser.models import (
    Section,
    SectionType,
    Task,
    TaskStatus,
)
from src.reporting.markdown_report import (
    render_markdown_report,
    render_overload_section
)


def test_render_markdown_report():
    section = Section(
        title="Doing",
        raw_title="Doing",
        type=SectionType.EXECUTION,
    )

    task = Task(
        title="Important Task",
        status=TaskStatus.OPEN,
        section=section,
        score=20,
    )

    board_metrics = BoardMetrics(
        total_tasks=10,
        active_tasks=5,
        actionable_tasks=6,
        overdue_tasks=1,
        total_score=100,
    )

    section_metrics = [
        SectionMetrics(
            section=section,
            summary=SectionSummary(
                total_tasks=5,
                active_tasks=5,
                actionable_tasks=5,
                completed_tasks=0,
                cancelled_tasks=0,
                scored_tasks=5,
                total_score=100,
            ),
            wip_limit=None,
        )
    ]

    board_health = BoardHealthReport(
        board_health_score=84.5,
        wip_violations=1,
        stale_task_count=2,
        top_priority_tasks=[
            PriorityScore(
                task=task,
                base_score=20,
                section_bonus=10,
                final_score=30,
            )
        ],
        top_attention_tasks=[
            AttentionScore(
                task=task,
                stale_score=4,
                due_score=6,
                final_score=10.0,
            )
        ],
        warnings=[
            HealthWarning(
                category="wip",
                message="Doing exceeds WIP limit",
            )
        ],
    )

    report = render_markdown_report(
        board_metrics=board_metrics,
        section_metrics=section_metrics,
        board_health=board_health,
    )

    assert "# Board Health Report" in report

    assert "Health Score: 84.5/100" in report

    assert "Important Task" in report

    assert "Doing exceeds WIP limit" in report

    assert "WIP Violations: 1" in report

    assert "Stale Tasks: 2" in report


def test_render_empty_report():
    report = render_markdown_report(
        board_metrics=BoardMetrics(),
        section_metrics=[],
        board_health=BoardHealthReport(
            board_health_score=100.0,
            wip_violations=0,
            stale_task_count=0,
            top_priority_tasks=[],
            top_attention_tasks=[],
            warnings=[],
        ),
    )

    assert "Health Score: 100.0/100" in report

    assert "No warnings" in report

    assert "No priority items" in report

    assert "No attention items" in report
    
    

class TestRenderOverloadSection:
    def test_empty_signals_returns_empty_string(self):
        """No signals means no section rendered."""
        assert render_overload_section([]) == ""

    def test_critical_signal_rendered_with_red_icon(self):
        """CRITICAL signals use red circle icon."""
        signals = [
            OverloadSignal(
                section_name="Dev",
                severity="CRITICAL",
                message="Section 'Dev' is OVER WIP limit (6/5 tasks).",
            )
        ]
        result = render_overload_section(signals)
        
        assert "🔴" in result
        assert "**Dev**" in result
        assert "OVER WIP limit" in result
        assert "Overload Warnings" in result

    def test_warning_signal_rendered_with_yellow_icon(self):
        """WARNING signals use yellow circle icon."""
        signals = [
            OverloadSignal(
                section_name="Review",
                severity="WARNING",
                message="Section 'Review' is nearing WIP limit.",
            )
        ]
        result = render_overload_section(signals)
        
        assert "🟡" in result
        assert "**Review**" in result

    def test_multiple_signals_rendered_as_list(self):
        """Multiple signals are rendered as a Markdown list."""
        signals = [
            OverloadSignal("Dev", "CRITICAL", "Over limit"),
            OverloadSignal("Review", "WARNING", "Near limit"),
        ]
        result = render_overload_section(signals)
        
        # Должны быть обе секции
        assert "**Dev**" in result
        assert "**Review**" in result
        # Должны быть обе иконки
        assert "🔴" in result
        assert "🟡" in result