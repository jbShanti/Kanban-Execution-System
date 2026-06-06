from src.analytics.models import ScoreCorridorSummary


def test_average_score_returns_zero_for_empty_corridor() -> None:
    corridor = ScoreCorridorSummary()

    assert corridor.average_score == 0.0


def test_average_score_returns_mean_value() -> None:
    corridor = ScoreCorridorSummary(
        scored_tasks=4,
        total_score=80,
    )

    assert corridor.average_score == 20.0


def test_percentage_of_returns_zero_when_total_tasks_is_zero() -> None:
    corridor = ScoreCorridorSummary(
        task_count=5,
    )

    assert corridor.percentage_of(0) == 0.0


def test_percentage_of_returns_percentage_of_total_tasks() -> None:
    corridor = ScoreCorridorSummary(
        task_count=5,
    )

    assert corridor.percentage_of(20) == 25.0