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
from src.reporting.sections.schedule_review_section import render_schedule_review_section
from datetime import date


def test_render_schedule_review_section_no_overdue():
    """Test rendering schedule review with no overdue tasks."""
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
        sections={},
    )
    
    report = ExecutionReport(
        schema_version="1.0",
        report_id="test-123",
        analysis_date=date(2026, 1, 15),
        board_health=board_health,
        board_summary=board_summary,
    )
    
    markdown = render_schedule_review_section(report)
    
    assert "## Schedule Review" in markdown
    assert "No overdue tasks" in markdown
    assert "Manageable Workload" in markdown


def test_render_schedule_review_section_with_overdue():
    """Test rendering schedule review with overdue tasks."""
    board_health = BoardHealth(
        total_tasks=15,
        active_tasks=12,
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
        active_tasks=12,
        actionable_tasks=10,
        completed_tasks=2,
        cancelled_tasks=1,
        overdue_tasks=3,
        scored_tasks=12,
        unscored_tasks=3,
        total_score=150,
        score_corridors={
            "21-25": ScoreCorridorSummary(task_count=2, scored_tasks=2, total_score=45),
            "16-20": ScoreCorridorSummary(task_count=3, scored_tasks=3, total_score=55),
            "no_score": ScoreCorridorSummary(task_count=3, scored_tasks=0, total_score=0),
        },
        sections={},
    )
    
    report = ExecutionReport(
        schema_version="1.0",
        report_id="test-123",
        analysis_date=date(2026, 1, 15),
        board_health=board_health,
        board_summary=board_summary,
    )
    
    markdown = render_schedule_review_section(report)
    
    assert "## Schedule Review" in markdown
    assert "3 task(s) overdue" in markdown
    assert "High Workload" in markdown or "Moderate Workload" in markdown
    assert "Urgent" in markdown


def test_render_schedule_review_section_high_workload():
    """Test rendering schedule review with high workload."""
    board_health = BoardHealth(
        total_tasks=25,
        active_tasks=20,
        score_coverage=0.7,
        tag_coverage=0.6,
        analytics_coverage=0.65,
        missing_score=7,
        missing_tag=10,
        orphan_tasks=5,
        sample_orphans=(),
        status=BoardHealthStatus.POOR,
    )
    
    board_summary = BoardSummary(
        total_tasks=25,
        active_tasks=20,
        actionable_tasks=18,
        completed_tasks=3,
        cancelled_tasks=2,
        overdue_tasks=5,
        scored_tasks=18,
        unscored_tasks=7,
        total_score=200,
        score_corridors={
            "21-25": ScoreCorridorSummary(task_count=5, scored_tasks=5, total_score=110),
            "16-20": ScoreCorridorSummary(task_count=5, scored_tasks=5, total_score=90),
            "no_score": ScoreCorridorSummary(task_count=7, scored_tasks=0, total_score=0),
        },
        sections={},
    )
    
    report = ExecutionReport(
        schema_version="1.0",
        report_id="test-123",
        analysis_date=date(2026, 1, 15),
        board_health=board_health,
        board_summary=board_summary,
    )
    
    markdown = render_schedule_review_section(report)
    
    assert "## Schedule Review" in markdown
    assert "High Workload" in markdown
    assert "5 task(s) overdue" in markdown
    assert "deferring or delegating" in markdown


def test_render_schedule_review_section_no_board_summary():
    """Test rendering schedule review when board summary is None."""
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
    
    markdown = render_schedule_review_section(report)
    
    assert "## Schedule Review" in markdown
    assert "not available" in markdown


def test_render_schedule_review_section_deterministic():
    """Test that schedule review section rendering is deterministic."""
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
        overdue_tasks=1,
        scored_tasks=9,
        unscored_tasks=1,
        total_score=100,
        score_corridors={
            "21-25": ScoreCorridorSummary(task_count=2, scored_tasks=2, total_score=45),
            "no_score": ScoreCorridorSummary(task_count=1, scored_tasks=0, total_score=0),
        },
        sections={},
    )
    
    report = ExecutionReport(
        schema_version="1.0",
        report_id="test-123",
        analysis_date=date(2026, 1, 15),
        board_health=board_health,
        board_summary=board_summary,
    )
    
    markdown1 = render_schedule_review_section(report)
    markdown2 = render_schedule_review_section(report)
    
    assert markdown1 == markdown2