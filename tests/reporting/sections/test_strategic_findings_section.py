from src.analytics.models import (
    BoardHealth,
    BoardHealthStatus,
    BoardSummary,
    ExecutionReport,
    ExecutiveSummary,
    MissingMetadata,
    OrphanTask,
    ScoreCorridorSummary,
    SectionSummary,
)
from src.reporting.sections.strategic_findings_section import render_strategic_findings_section
from datetime import date


def test_render_strategic_findings_section_with_executive_summary():
    """Test rendering strategic findings with executive summary."""
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
            "no_score": ScoreCorridorSummary(task_count=2, scored_tasks=0, total_score=0),
        },
        sections={},
    )
    
    executive_summary = ExecutiveSummary(
        summary="Board is in good health with strong focus on high-value work. One overdue task needs attention."
    )
    
    report = ExecutionReport(
        schema_version="1.0",
        report_id="test-123",
        analysis_date=date(2026, 1, 15),
        board_health=board_health,
        board_summary=board_summary,
        executive_summary=executive_summary,
    )
    
    markdown = render_strategic_findings_section(report)
    
    assert "## Strategic Findings" in markdown
    assert "Executive Summary" in markdown
    assert "good health" in markdown
    assert "overdue task needs attention" in markdown
    assert "Key Risks" in markdown
    assert "Key Opportunities" in markdown
    assert "Recommended Actions for Today" in markdown


def test_render_strategic_findings_section_without_executive_summary():
    """Test rendering strategic findings without executive summary (auto-generated)."""
    board_health = BoardHealth(
        total_tasks=15,
        active_tasks=10,
        score_coverage=0.7,
        tag_coverage=0.6,
        analytics_coverage=0.65,
        missing_score=4,
        missing_tag=6,
        orphan_tasks=3,
        sample_orphans=(),
        status=BoardHealthStatus.WARNING,
    )
    
    board_summary = BoardSummary(
        total_tasks=15,
        active_tasks=10,
        actionable_tasks=9,
        completed_tasks=3,
        cancelled_tasks=2,
        overdue_tasks=2,
        scored_tasks=11,
        unscored_tasks=4,
        total_score=150,
        score_corridors={
            "21-25": ScoreCorridorSummary(task_count=2, scored_tasks=2, total_score=45),
            "16-20": ScoreCorridorSummary(task_count=3, scored_tasks=3, total_score=55),
            "no_score": ScoreCorridorSummary(task_count=4, scored_tasks=0, total_score=0),
        },
        sections={},
    )
    
    report = ExecutionReport(
        schema_version="1.0",
        report_id="test-123",
        analysis_date=date(2026, 1, 15),
        board_health=board_health,
        board_summary=board_summary,
        executive_summary=None,
    )
    
    markdown = render_strategic_findings_section(report)
    
    assert "## Strategic Findings" in markdown
    assert "Executive Summary" in markdown
    assert "15 total tasks" in markdown
    assert "10 active" in markdown
    assert "Warning" in markdown
    assert "2 overdue tasks" in markdown
    assert "Key Risks" in markdown
    assert "Overdue Work" in markdown
    assert "Scoring Gaps" in markdown


def test_render_strategic_findings_section_healthy_board():
    """Test rendering strategic findings for a healthy board."""
    board_health = BoardHealth(
        total_tasks=10,
        active_tasks=5,
        score_coverage=0.95,
        tag_coverage=0.9,
        analytics_coverage=0.9,
        missing_score=0,
        missing_tag=1,
        orphan_tasks=0,
        sample_orphans=(),
        status=BoardHealthStatus.EXCELLENT,
    )
    
    board_summary = BoardSummary(
        total_tasks=10,
        active_tasks=5,
        actionable_tasks=5,
        completed_tasks=4,
        cancelled_tasks=1,
        overdue_tasks=0,
        scored_tasks=10,
        unscored_tasks=0,
        total_score=120,
        score_corridors={
            "21-25": ScoreCorridorSummary(task_count=2, scored_tasks=2, total_score=45),
            "16-20": ScoreCorridorSummary(task_count=3, scored_tasks=3, total_score=55),
            "11-15": ScoreCorridorSummary(task_count=3, scored_tasks=3, total_score=35),
            "6-10": ScoreCorridorSummary(task_count=2, scored_tasks=2, total_score=15),
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
    
    markdown = render_strategic_findings_section(report)
    
    assert "## Strategic Findings" in markdown
    assert "Excellent" in markdown
    assert "No critical risks identified" in markdown
    assert "High-Value Portfolio" in markdown
    assert "High Data Quality" in markdown
    assert "Clean Board" in markdown
    assert "Advance high-value work" in markdown


def test_render_strategic_findings_section_no_board_summary():
    """Test rendering strategic findings when board summary is None."""
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
    
    markdown = render_strategic_findings_section(report)
    
    assert "## Strategic Findings" in markdown
    assert "not available" in markdown


def test_render_strategic_findings_section_deterministic():
    """Test that strategic findings section rendering is deterministic."""
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
    
    markdown1 = render_strategic_findings_section(report)
    markdown2 = render_strategic_findings_section(report)
    
    assert markdown1 == markdown2