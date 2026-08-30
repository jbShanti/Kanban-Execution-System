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
from src.reporting.sections.task_analysis_section import render_task_analysis_section
from datetime import date


def test_render_task_analysis_section_normal():
    """Test rendering task analysis with normal data."""
    board_health = BoardHealth(
        total_tasks=20,
        active_tasks=8,
        score_coverage=0.9,
        tag_coverage=0.8,
        analytics_coverage=0.85,
        missing_score=2,
        missing_tag=4,
        orphan_tasks=1,
        sample_orphans=(),
        status=BoardHealthStatus.GOOD,
    )
    
    board_summary = BoardSummary(
        total_tasks=20,
        active_tasks=8,
        actionable_tasks=8,
        completed_tasks=7,
        cancelled_tasks=5,
        overdue_tasks=1,
        scored_tasks=18,
        unscored_tasks=2,
        total_score=250,
        score_corridors={
            "21-25": ScoreCorridorSummary(task_count=3, scored_tasks=3, total_score=70),
            "16-20": ScoreCorridorSummary(task_count=4, scored_tasks=4, total_score=70),
            "11-15": ScoreCorridorSummary(task_count=5, scored_tasks=5, total_score=60),
            "6-10": ScoreCorridorSummary(task_count=3, scored_tasks=3, total_score=25),
            "1-5": ScoreCorridorSummary(task_count=3, scored_tasks=3, total_score=10),
            "no_score": ScoreCorridorSummary(task_count=2, scored_tasks=0, total_score=0),
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
    
    markdown = render_task_analysis_section(report)
    
    assert "## Task Analysis" in markdown
    assert "Task Status Overview" in markdown
    assert "**Total Tasks**: 20" in markdown
    assert "**Active**: 8" in markdown
    assert "**Overdue**: 1" in markdown
    assert "Ready for Execution" in markdown
    assert "8 actionable task(s)" in markdown
    assert "Risk Assessment" in markdown


def test_render_task_analysis_section_high_risk():
    """Test rendering task analysis with high risk indicators."""
    board_health = BoardHealth(
        total_tasks=30,
        active_tasks=20,
        score_coverage=0.6,
        tag_coverage=0.5,
        analytics_coverage=0.55,
        missing_score=12,
        missing_tag=15,
        orphan_tasks=8,
        sample_orphans=(),
        status=BoardHealthStatus.POOR,
    )
    
    board_summary = BoardSummary(
        total_tasks=30,
        active_tasks=20,
        actionable_tasks=18,
        completed_tasks=5,
        cancelled_tasks=5,
        overdue_tasks=5,
        scored_tasks=18,
        unscored_tasks=12,
        total_score=200,
        score_corridors={
            "21-25": ScoreCorridorSummary(task_count=8, scored_tasks=8, total_score=180),
            "16-20": ScoreCorridorSummary(task_count=5, scored_tasks=5, total_score=90),
            "no_score": ScoreCorridorSummary(task_count=12, scored_tasks=0, total_score=0),
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
    
    markdown = render_task_analysis_section(report)
    
    assert "## Task Analysis" in markdown
    assert "5 overdue task(s)" in markdown
    assert "High:" in markdown  # High risk indicators
    assert "focus dilution" in markdown
    assert "prioritization blind spots" in markdown


def test_render_task_analysis_section_no_actionable():
    """Test rendering task analysis with no actionable tasks."""
    board_health = BoardHealth(
        total_tasks=10,
        active_tasks=0,
        score_coverage=0.8,
        tag_coverage=0.7,
        analytics_coverage=0.75,
        missing_score=2,
        missing_tag=3,
        orphan_tasks=1,
        sample_orphans=(),
        status=BoardHealthStatus.GOOD,
    )
    
    board_summary = BoardSummary(
        total_tasks=10,
        active_tasks=0,
        actionable_tasks=0,
        completed_tasks=8,
        cancelled_tasks=2,
        overdue_tasks=0,
        scored_tasks=8,
        unscored_tasks=2,
        total_score=100,
        score_corridors={
            "21-25": ScoreCorridorSummary(task_count=1, scored_tasks=1, total_score=22),
            "no_score": ScoreCorridorSummary(task_count=2, scored_tasks=0, total_score=0),
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
    
    markdown = render_task_analysis_section(report)
    
    assert "## Task Analysis" in markdown
    assert "No actionable tasks currently" in markdown
    assert "Moving tasks from Scheduled/Queued" in markdown


def test_render_task_analysis_section_no_board_summary():
    """Test rendering task analysis when board summary is None."""
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
    
    markdown = render_task_analysis_section(report)
    
    assert "## Task Analysis" in markdown
    assert "not available" in markdown


def test_render_task_analysis_section_deterministic():
    """Test that task analysis section rendering is deterministic."""
    board_health = BoardHealth(
        total_tasks=20,
        active_tasks=8,
        score_coverage=0.9,
        tag_coverage=0.8,
        analytics_coverage=0.85,
        missing_score=2,
        missing_tag=4,
        orphan_tasks=1,
        sample_orphans=(),
        status=BoardHealthStatus.GOOD,
    )
    
    board_summary = BoardSummary(
        total_tasks=20,
        active_tasks=8,
        actionable_tasks=8,
        completed_tasks=7,
        cancelled_tasks=5,
        overdue_tasks=1,
        scored_tasks=18,
        unscored_tasks=2,
        total_score=250,
        score_corridors={
            "21-25": ScoreCorridorSummary(task_count=3, scored_tasks=3, total_score=70),
            "no_score": ScoreCorridorSummary(task_count=2, scored_tasks=0, total_score=0),
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
    
    markdown1 = render_task_analysis_section(report)
    markdown2 = render_task_analysis_section(report)
    
    assert markdown1 == markdown2