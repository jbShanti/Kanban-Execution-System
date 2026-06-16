from src.analytics.models import (
    BoardHealth,
    BoardHealthStatus,
    MissingMetadata,
    OrphanTask,
)

from src.reporting.sections.board_health_section import (
    render_board_health_section,
)


def test_render_board_health_section() -> None:

    board_health = BoardHealth(
        total_tasks=100,
        score_coverage=0.95,
        tag_coverage=0.90,
        analytics_coverage=0.90,
        missing_score=5,
        missing_tag=10,
        orphan_tasks=12,
        sample_orphans=(
            OrphanTask(
                title="Task A",
                is_active=True,
                missing=(
                    MissingMetadata.SCORE,
                    MissingMetadata.TAG,
                ),
            ),
            OrphanTask(
                title="Task B",
                is_active=False,
                missing=(
                    MissingMetadata.TAG,
                ),
            ),
        ),
        status=BoardHealthStatus.GOOD,
    )

    markdown = render_board_health_section(
        board_health
    )

    assert "## 1. Board Health" in markdown

    assert "- Status: Good" in markdown

    assert (
        "- Analytics Coverage: 90.0%"
        in markdown
    )

    assert (
        "- Score Coverage: 95.0%"
        in markdown
    )

    assert (
        "- Tag Coverage: 90.0%"
        in markdown
    )

    assert "- Orphan Tasks: 12" in markdown

    assert "- Missing Score: 5" in markdown

    assert "- Missing Tags: 10" in markdown

    assert "### Sample Orphans" in markdown

    assert "Task A" in markdown
    assert "Task B" in markdown

    assert "Active" in markdown
    assert "Inactive" in markdown
    
    
def test_render_board_health_section_without_orphans() -> None:

    board_health = BoardHealth(
        total_tasks=100,
        score_coverage=1.0,
        tag_coverage=1.0,
        analytics_coverage=1.0,
        missing_score=0,
        missing_tag=0,
        orphan_tasks=0,
        sample_orphans=(),
        status=BoardHealthStatus.EXCELLENT,
    )

    markdown = render_board_health_section(
        board_health
    )

    assert "## 1. Board Health" in markdown

    assert "- Status: Excellent" in markdown

    assert (
        "- Analytics Coverage: 100.0%"
        in markdown
    )

    assert (
        "- Score Coverage: 100.0%"
        in markdown
    )

    assert (
        "- Tag Coverage: 100.0%"
        in markdown
    )

    assert "- Orphan Tasks: 0" in markdown

    assert "- Missing Score: 0" in markdown

    assert "- Missing Tags: 0" in markdown

    assert "### Sample Orphans" not in markdown
    
    
from datetime import datetime

from src.analytics.models import (
    AnalyticsReport,
    BoardHealth,
    BoardHealthStatus,
)

from src.reporting.analytics_report_renderer import (
    render_analytics_report,
)


def test_render_analytics_report_includes_board_health_section() -> None:

    board_health = BoardHealth(
        total_tasks=100,
        score_coverage=0.95,
        tag_coverage=0.90,
        analytics_coverage=0.90,
        missing_score=5,
        missing_tag=10,
        orphan_tasks=12,
        sample_orphans=(),
        status=BoardHealthStatus.GOOD,
    )

    report = AnalyticsReport(
        global_score=100,
        corridors=[],
        total_tasks=100,
        scored_tasks=95,
        focus_tasks=10,
        focus_percentage=10.0,
        high_value_tasks=20,
        high_value_percentage=20.0,
        board_health=board_health,
        generated_at=datetime.now(),
    )

    markdown = render_analytics_report(report)

    assert "# Analytics Report" in markdown

    assert "## 1. Board Health" in markdown

    assert "Analytics Coverage" in markdown
    assert "Score Coverage" in markdown
    assert "Tag Coverage" in markdown

    assert "Status: Good" in markdown
    
    
from datetime import datetime

from src.analytics.models import (
    AnalyticsReport,
    BoardHealth,
    BoardHealthStatus,
    ScoreCorridor,
)

from src.reporting.sections.score_corridors_section import (
    render_score_corridors_section,
)


def test_render_score_corridors_section() -> None:

    report = AnalyticsReport(
        global_score=101,
        corridors=[
            ScoreCorridor(
                name="21-25",
                task_count=2,
                total_score=47,
                average_score=23.5,
                percentage=20.0,
                score_share_percentage=35.6,
            ),
            ScoreCorridor(
                name="16-20",
                task_count=3,
                total_score=54,
                average_score=18.0,
                percentage=30.0,
                score_share_percentage=40.9,
            ),
        ],
        total_tasks=10,
        scored_tasks=8,
        focus_tasks=2,
        focus_percentage=20.0,
        high_value_tasks=5,
        high_value_percentage=50.0,
        board_health=BoardHealth(
            total_tasks=10,
            score_coverage=0.8,
            tag_coverage=0.8,
            analytics_coverage=0.8,
            missing_score=2,
            missing_tag=2,
            orphan_tasks=1,
            sample_orphans=(),
            status=BoardHealthStatus.GOOD,
        ),
        generated_at=datetime.now(),
    )

    markdown = render_score_corridors_section(
        report
    )

    assert "## 2. Score Corridors" in markdown

    assert (
        "- 21-25: 2 tasks (20.0%)"
        in markdown
    )

    assert (
        "- 16-20: 3 tasks (30.0%)"
        in markdown
    )

    assert (
        "- Focus Tasks (21-25): 2 (20.0%)"
        in markdown
    )

    assert (
        "- High Value Tasks (16-25): 5 (50.0%)"
        in markdown
    )
    
    
def test_render_score_corridors_section_without_corridors() -> None:

    report = AnalyticsReport(
        global_score=0,
        corridors=[],
        total_tasks=0,
        scored_tasks=0,
        focus_tasks=0,
        focus_percentage=0.0,
        high_value_tasks=0,
        high_value_percentage=0.0,
        board_health=BoardHealth(
            total_tasks=0,
            score_coverage=0.0,
            tag_coverage=0.0,
            analytics_coverage=0.0,
            missing_score=0,
            missing_tag=0,
            orphan_tasks=0,
            sample_orphans=(),
            status=BoardHealthStatus.CRITICAL,
        ),
        generated_at=datetime.now(),
    )

    markdown = render_score_corridors_section(
        report
    )

    assert "## 2. Score Corridors" in markdown

    assert (
        "No score corridor data available."
        in markdown
    )

    assert "Focus Tasks" not in markdown

    assert "High Value Tasks" not in markdown