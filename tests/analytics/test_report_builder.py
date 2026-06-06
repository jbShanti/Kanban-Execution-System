from src.analytics.models import (
    AnalyticsReport,
    AnalyticsSnapshot,
    BoardSummary,
    BoardMetrics,
)
from src.analytics.report_builder import build_analytics_report


def test_build_analytics_report_returns_analytics_report() -> None:
    snapshot = AnalyticsSnapshot(
        summary=BoardSummary(),
        board=BoardMetrics(),
        sections={},
    )

    report = build_analytics_report(snapshot)

    assert isinstance(report, AnalyticsReport)
    
    

    
def test_build_analytics_report_populates_fields() -> None:
    from src.analytics.models import ScoreCorridorSummary

    snapshot = AnalyticsSnapshot(
        summary=BoardSummary(
            total_tasks=10,
            scored_tasks=8,
            total_score=120,
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
    )

    report = build_analytics_report(snapshot)

    assert report.total_tasks == 10
    assert report.scored_tasks == 8
    assert report.global_score == 120
    
    corridor = next(
    c
    for c in report.corridors
    if c.name == "21-25"
    )

    assert corridor.task_count == 2
    assert corridor.total_score == 47
    assert corridor.average_score == 23.5
    assert corridor.percentage == 20.0