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
from src.reporting.sections.corridor_analysis_section import render_corridor_analysis_section
from datetime import date


def test_render_corridor_analysis_section_full():
    """Test rendering corridor analysis with full data."""
    board_health = BoardHealth(
        total_tasks=20,
        active_tasks=10,
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
        active_tasks=10,
        actionable_tasks=10,
        completed_tasks=5,
        cancelled_tasks=5,
        overdue_tasks=1,
        scored_tasks=18,
        unscored_tasks=2,
        total_score=250,
        score_corridors={
            "21-25": ScoreCorridorSummary(task_count=4, scored_tasks=4, total_score=90),
            "16-20": ScoreCorridorSummary(task_count=5, scored_tasks=5, total_score=90),
            "11-15": ScoreCorridorSummary(task_count=4, scored_tasks=4, total_score=50),
            "6-10": ScoreCorridorSummary(task_count=3, scored_tasks=3, total_score=20),
            "1-5": ScoreCorridorSummary(task_count=2, scored_tasks=2, total_score=8),
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
    
    markdown = render_corridor_analysis_section(report)
    
    assert "## Corridor Analysis" in markdown
    assert "Critical (21-25)" in markdown
    assert "High (16-20)" in markdown
    assert "Medium (11-15)" in markdown
    assert "Low (6-10)" in markdown
    assert "Optional (1-5)" in markdown
    assert "No Score" in markdown
    assert "4 tasks" in markdown  # critical tasks
    assert "5 tasks" in markdown  # high tasks
    assert "Summary" in markdown
    assert "**Critical Focus Tasks (21-25)**: 4 (20.0%)" in markdown
    assert "**High Value Tasks (16-25)**: 9 (45.0%)" in markdown


def test_render_corridor_analysis_section_empty():
    """Test rendering corridor analysis with no data."""
    board_health = BoardHealth(
        total_tasks=0,
        active_tasks=0,
        score_coverage=0.0,
        tag_coverage=0.0,
        analytics_coverage=0.0,
        missing_score=0,
        missing_tag=0,
        orphan_tasks=0,
        sample_orphans=(),
        status=BoardHealthStatus.CRITICAL,
    )
    
    board_summary = BoardSummary(
        total_tasks=0,
        active_tasks=0,
        actionable_tasks=0,
        completed_tasks=0,
        cancelled_tasks=0,
        overdue_tasks=0,
        scored_tasks=0,
        unscored_tasks=0,
        total_score=0,
        score_corridors={},
        sections={},
    )
    
    report = ExecutionReport(
        schema_version="1.0",
        report_id="test-123",
        analysis_date=date(2026, 1, 15),
        board_health=board_health,
        board_summary=board_summary,
    )
    
    markdown = render_corridor_analysis_section(report)
    
    assert "## Corridor Analysis" in markdown
    assert "No score corridor data available" in markdown


def test_render_corridor_analysis_section_no_board_summary():
    """Test rendering corridor analysis when board summary is None."""
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
    
    markdown = render_corridor_analysis_section(report)
    
    assert "## Corridor Analysis" in markdown
    assert "not available" in markdown


def test_render_corridor_analysis_section_deterministic():
    """Test that corridor analysis section rendering is deterministic."""
    board_health = BoardHealth(
        total_tasks=20,
        active_tasks=10,
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
        active_tasks=10,
        actionable_tasks=10,
        completed_tasks=5,
        cancelled_tasks=5,
        overdue_tasks=1,
        scored_tasks=18,
        unscored_tasks=2,
        total_score=250,
        score_corridors={
            "21-25": ScoreCorridorSummary(task_count=4, scored_tasks=4, total_score=90),
            "16-20": ScoreCorridorSummary(task_count=5, scored_tasks=5, total_score=90),
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
    
    markdown1 = render_corridor_analysis_section(report)
    markdown2 = render_corridor_analysis_section(report)
    
    assert markdown1 == markdown2