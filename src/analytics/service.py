from src.analytics.calculators.status_metrics import (
    calculate_status_metrics,
)
from src.analytics.calculators.time_metrics import (
    calculate_time_metrics,
)
from src.analytics.calculators.score_metrics import (
    calculate_score_metrics,
)

from src.analytics.models import TaskMetrics
from src.parser.models import Task


def calculate_task_metrics(
    tasks: list[Task],
) -> TaskMetrics:
    status_metrics = calculate_status_metrics(
        tasks,
    )

    time_metrics = calculate_time_metrics(
        tasks,
    )

    score_metrics = calculate_score_metrics(
        tasks,
    )

    return TaskMetrics(
        **status_metrics,
        **time_metrics,
        **score_metrics,
    )