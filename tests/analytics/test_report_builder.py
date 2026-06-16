from src.analytics.models import (
    AnalyticsReport,
    AnalyticsSnapshot,
    BoardSummary,
    BoardMetrics,
    BoardHealth,
    BoardHealthStatus,
)
from src.analytics.report_builder import build_analytics_report


def test_build_analytics_report_returns_analytics_report() -> None:
    snapshot = AnalyticsSnapshot(
        summary=BoardSummary(),
        board=BoardMetrics(),
        sections={},
        board_health=BoardHealth(
            total_tasks=0,

            score_coverage=1.0,
            tag_coverage=1.0,
            analytics_coverage=1.0,

            missing_score=0,
            missing_tag=0,

            orphan_tasks=0,

            sample_orphans=(),

            status=BoardHealthStatus.EXCELLENT,
        ),
    )

    report = build_analytics_report(snapshot)

    assert isinstance(report, AnalyticsReport)
    
    

    
def test_build_analytics_report_populates_fields() -> None:
    from src.analytics.models import ScoreCorridorSummary
    
    EMPTY_BOARD_HEALTH = BoardHealth(
        total_tasks=0,

        score_coverage=1.0,
        tag_coverage=1.0,
        analytics_coverage=1.0,

        missing_score=0,
        missing_tag=0,

        orphan_tasks=0,

        sample_orphans=(),

        status=BoardHealthStatus.EXCELLENT,
    )

    snapshot = AnalyticsSnapshot(
        summary=BoardSummary(
            total_tasks=10,
            scored_tasks=8,
            total_score=132,
            score_corridors={
                "21-25": ScoreCorridorSummary(
                    task_count=2,
                    scored_tasks=2,
                    total_score=47,
                ),
                "16-20": ScoreCorridorSummary(
                    task_count=3,
                    scored_tasks=3,
                    total_score=54,
                ),
                "11-15": ScoreCorridorSummary(
                    task_count=2,
                    scored_tasks=2,
                    total_score=24,
                ),
                "6-10": ScoreCorridorSummary(
                    task_count=1,
                    scored_tasks=1,
                    total_score=7,
                ),
                "1-5": ScoreCorridorSummary(),
                "0": ScoreCorridorSummary(),
                "no_score": ScoreCorridorSummary(
                    task_count=2,
                ),
            },
        ),
        board=BoardMetrics(),
        sections={},
        board_health=EMPTY_BOARD_HEALTH,
    )

    report = build_analytics_report(snapshot)

    assert report.total_tasks == 10
    assert report.scored_tasks == 8
    assert report.global_score == 132
    
    corridor = next(
    c
    for c in report.corridors
    if c.name == "21-25"
    )

    assert corridor.task_count == 2
    assert corridor.total_score == 47
    assert corridor.average_score == 23.5
    assert corridor.percentage == 20.0
    
    assert report.high_value_tasks == 5
    assert report.high_value_percentage == 50.0
    
    assert report.focus_tasks == 2
    assert report.focus_percentage == 20.0
    
    focus_corridor = next(
        corridor
        for corridor in report.corridors
        if corridor.name == "21-25"
    )

    expected_share = 47 / 132 * 100

    assert (
        abs(
            focus_corridor.score_share_percentage
            - expected_share
        )
        < 0.0001
    )
    
    
      
     
    total_share = sum(
    corridor.score_share_percentage
    for corridor in report.corridors
)

    assert abs(total_share - 100.0) < 0.01

    
    
def test_build_analytics_report_preserves_board_health() -> None:

    board_health = BoardHealth(
        total_tasks=10,
        score_coverage=0.8,
        tag_coverage=0.7,
        analytics_coverage=0.6,
        missing_score=2,
        missing_tag=3,
        orphan_tasks=4,
        sample_orphans=(),
        status=BoardHealthStatus.POOR,
    )

    snapshot = AnalyticsSnapshot(
        summary=BoardSummary(),
        board=BoardMetrics(),
        sections={},
        board_health=board_health,
    )

    report = build_analytics_report(snapshot)

    assert report.board_health is board_health