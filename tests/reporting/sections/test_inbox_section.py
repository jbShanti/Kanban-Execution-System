from src.analytics.models import (
    BoardHealth,
    BoardHealthStatus,
    BoardSummary,
    ExecutionReport,
    MissingMetadata,
    OrphanTask,
    ScoreCorridorSummary,
    SectionSummary,
)
from src.reporting.sections.inbox_section import render_inbox_section
from datetime import date


def test_render_inbox_section_empty():
    """Test rendering inbox section with no inbox tasks."""
    board_health = BoardHealth(
        total_tasks=10,
        active_tasks=5,
        score_coverage=0.9,
        tag_coverage=0.8,
        analytics_coverage=0.85,
        missing_score=1,
        missing_tag=2,
        orphan_tasks=0,
        sample_orphans=(),
        status=BoardHealthStatus.GOOD,
    )
    
    board_summary = BoardSummary(
        total_tasks=10,
        active_tasks=5,
        actionable_tasks=5,
        completed_tasks=3,
        cancelled_tasks=2,
        overdue_tasks=0,
        scored_tasks=9,
        unscored_tasks=1,
        total_score=100,
        score_corridors={
            "21-25": ScoreCorridorSummary(task_count=2, scored_tasks=2, total_score=45),
            "16-20": ScoreCorridorSummary(task_count=3, scored_tasks=3, total_score=55),
            "no_score": ScoreCorridorSummary(task_count=1, scored_tasks=0, total_score=0),
        },
        sections={
            "Doing": SectionSummary(total_tasks=5, active_tasks=5, actionable_tasks=5, scored_tasks=5, total_score=100),
        },
    )
    
    report = ExecutionReport(
        schema_version="1.0",
        report_id="test-123",
        analysis_date=date(2026, 1, 15),
        board_health=board_health,
        board_summary=board_summary,
    )
    
    markdown = render_inbox_section(report)
    
    assert "## Inbox" in markdown
    assert "Inbox is clear" in markdown


def test_render_inbox_section_with_tasks():
    """Test rendering inbox section with inbox tasks."""
    board_health = BoardHealth(
        total_tasks=15,
        active_tasks=8,
        score_coverage=0.8,
        tag_coverage=0.7,
        analytics_coverage=0.75,
        missing_score=3,
        missing_tag=4,
        orphan_tasks=2,
        sample_orphans=(),
        status=BoardHealthStatus.WARNING,
    )
    
    board_summary = BoardSummary(
        total_tasks=15,
        active_tasks=8,
        actionable_tasks=8,
        completed_tasks=5,
        cancelled_tasks=2,
        overdue_tasks=1,
        scored_tasks=12,
        unscored_tasks=3,
        total_score=150,
        score_corridors={
            "21-25": ScoreCorridorSummary(task_count=2, scored_tasks=2, total_score=45),
            "16-20": ScoreCorridorSummary(task_count=3, scored_tasks=3, total_score=55),
            "no_score": ScoreCorridorSummary(task_count=3, scored_tasks=0, total_score=0),
        },
        sections={
            "Inbox": SectionSummary(total_tasks=3, active_tasks=3, actionable_tasks=3, scored_tasks=1, total_score=10),
            "Doing": SectionSummary(total_tasks=5, active_tasks=5, actionable_tasks=5, scored_tasks=5, total_score=100),
        },
    )
    
    report = ExecutionReport(
        schema_version="1.0",
        report_id="test-123",
        analysis_date=date(2026, 1, 15),
        board_health=board_health,
        board_summary=board_summary,
    )
    
    markdown = render_inbox_section(report)
    
    assert "## Inbox" in markdown
    assert "3 unprocessed task(s)" in markdown
    assert "Active: 3" in markdown
    assert "Actionable: 3" in markdown


def test_render_inbox_section_no_board_summary():
    """Test rendering inbox section when board summary is None."""
    board_health = BoardHealth(
        total_tasks=10,
        active_tasks=5,
        score_coverage=0.9,
        tag_coverage=0.8,
        analytics_coverage=0.85,
        missing_score=1,
        missing_tag=2,
        orphan_tasks=0,
        sample_orphans=(),
        status=BoardHealthStatus.GOOD,
    )
    
    report = ExecutionReport(
        schema_version="1.0",
        report_id="test-123",
        analysis_date=date(2026, 1, 15),
        board_health=board_health,
        board_summary=None,
    )
    
    markdown = render_inbox_section(report)
    
    assert "## Inbox" in markdown
    assert "not available" in markdown


def test_render_inbox_section_deterministic():
    """Test that inbox section rendering is deterministic."""
    board_health = BoardHealth(
        total_tasks=10,
        active_tasks=5,
        score_coverage=0.9,
        tag_coverage=0.8,
        analytics_coverage=0.85,
        missing_score=1,
        missing_tag=2,
        orphan_tasks=0,
        sample_orphans=(),
        status=BoardHealthStatus.GOOD,
    )
    
    board_summary = BoardSummary(
        total_tasks=10,
        active_tasks=5,
        actionable_tasks=5,
        completed_tasks=3,
        cancelled_tasks=2,
        overdue_tasks=0,
        scored_tasks=9,
        unscored_tasks=1,
        total_score=100,
        score_corridors={
            "21-25": ScoreCorridorSummary(task_count=2, scored_tasks=2, total_score=45),
            "no_score": ScoreCorridorSummary(task_count=1, scored_tasks=0, total_score=0),
        },
        sections={
            "Inbox": SectionSummary(total_tasks=2, active_tasks=2, actionable_tasks=2, scored_tasks=1, total_score=10),
        },
    )
    
    report = ExecutionReport(
        schema_version="1.0",
        report_id="test-123",
        analysis_date=date(2026, 1, 15),
        board_health=board_health,
        board_summary=board_summary,
    )
    
    markdown1 = render_inbox_section(report)
    markdown2 = render_inbox_section(report)
    
    assert markdown1 == markdown2