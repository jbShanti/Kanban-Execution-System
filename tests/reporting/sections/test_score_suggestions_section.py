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
from src.reporting.sections.score_suggestions_section import render_score_suggestions_section
from datetime import date


def test_render_score_suggestions_section_with_issues():
    """Test rendering score suggestions with scoring issues."""
    board_health = BoardHealth(
        total_tasks=20,
        active_tasks=10,
        score_coverage=0.7,
        tag_coverage=0.8,
        analytics_coverage=0.75,
        missing_score=6,
        missing_tag=4,
        orphan_tasks=2,
        sample_orphans=(),
        status=BoardHealthStatus.WARNING,
    )
    
    board_summary = BoardSummary(
        total_tasks=20,
        active_tasks=10,
        actionable_tasks=10,
        completed_tasks=5,
        cancelled_tasks=5,
        overdue_tasks=1,
        scored_tasks=14,
        unscored_tasks=6,
        total_score=200,
        score_corridors={
            "21-25": ScoreCorridorSummary(task_count=8, scored_tasks=8, total_score=180),  # Too many critical
            "16-20": ScoreCorridorSummary(task_count=2, scored_tasks=2, total_score=35),
            "1-5": ScoreCorridorSummary(task_count=2, scored_tasks=2, total_score=8),
            "0": ScoreCorridorSummary(task_count=2, scored_tasks=2, total_score=0),  # Zero score tasks
            "no_score": ScoreCorridorSummary(task_count=6, scored_tasks=0, total_score=0),
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
    
    markdown = render_score_suggestions_section(report)
    
    assert "## Score Suggestions" in markdown
    assert "Tasks Requiring Score" in markdown
    assert "6 task(s) without score" in markdown
    assert "Score Distribution Analysis" in markdown
    assert "Zero Score" in markdown
    assert "Critical Overload" in markdown
    assert "Recommendations" in markdown


def test_render_score_suggestions_section_healthy():
    """Test rendering score suggestions with healthy scoring."""
    board_health = BoardHealth(
        total_tasks=15,
        active_tasks=8,
        score_coverage=0.95,
        tag_coverage=0.9,
        analytics_coverage=0.9,
        missing_score=1,
        missing_tag=1,
        orphan_tasks=0,
        sample_orphans=(),
        status=BoardHealthStatus.EXCELLENT,
    )
    
    board_summary = BoardSummary(
        total_tasks=15,
        active_tasks=8,
        actionable_tasks=8,
        completed_tasks=4,
        cancelled_tasks=3,
        overdue_tasks=0,
        scored_tasks=14,
        unscored_tasks=1,
        total_score=180,
        score_corridors={
            "21-25": ScoreCorridorSummary(task_count=2, scored_tasks=2, total_score=45),
            "16-20": ScoreCorridorSummary(task_count=3, scored_tasks=3, total_score=55),
            "11-15": ScoreCorridorSummary(task_count=4, scored_tasks=4, total_score=50),
            "6-10": ScoreCorridorSummary(task_count=3, scored_tasks=3, total_score=20),
            "1-5": ScoreCorridorSummary(task_count=2, scored_tasks=2, total_score=8),
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
    
    markdown = render_score_suggestions_section(report)
    
    assert "## Score Suggestions" in markdown
    assert "1 task(s) without score" in markdown
    assert "No Score" in markdown
    assert "Recommendations" in markdown


def test_render_score_suggestions_section_no_board_summary():
    """Test rendering score suggestions when board summary is None."""
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
    
    markdown = render_score_suggestions_section(report)
    
    assert "## Score Suggestions" in markdown
    assert "not available" in markdown


def test_render_score_suggestions_section_deterministic():
    """Test that score suggestions section rendering is deterministic."""
    board_health = BoardHealth(
        total_tasks=20,
        active_tasks=10,
        score_coverage=0.7,
        tag_coverage=0.8,
        analytics_coverage=0.75,
        missing_score=6,
        missing_tag=4,
        orphan_tasks=2,
        sample_orphans=(),
        status=BoardHealthStatus.WARNING,
    )
    
    board_summary = BoardSummary(
        total_tasks=20,
        active_tasks=10,
        actionable_tasks=10,
        completed_tasks=5,
        cancelled_tasks=5,
        overdue_tasks=1,
        scored_tasks=14,
        unscored_tasks=6,
        total_score=200,
        score_corridors={
            "21-25": ScoreCorridorSummary(task_count=8, scored_tasks=8, total_score=180),
            "no_score": ScoreCorridorSummary(task_count=6, scored_tasks=0, total_score=0),
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
    
    markdown1 = render_score_suggestions_section(report)
    markdown2 = render_score_suggestions_section(report)
    
    assert markdown1 == markdown2