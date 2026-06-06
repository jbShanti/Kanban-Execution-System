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
    snapshot = AnalyticsSnapshot(
        summary=BoardSummary(
            total_tasks=10,
            scored_tasks=8,
            total_score=120,
            score_distribution={
                "21-25": 2,
                "16-20": 3,
                "11-15": 2,
                "6-10": 1,
                "1-5": 0,
                "0": 0,
                "no_score": 2,
            },
        ),
        board=BoardMetrics(),
        sections={},
    )

    report = build_analytics_report(snapshot)

    assert report.total_tasks == 10
    assert report.scored_tasks == 8
    assert report.global_score == 120
    assert report.corridor_distribution["21-25"] == 2