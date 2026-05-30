from dataclasses import dataclass, field
from src.parser.models import Section
from typing import Mapping

@dataclass(slots=True)
class BoardMetrics:
    total_tasks: int = 0

    active_tasks: int = 0
    actionable_tasks: int = 0

    open_tasks: int = 0
    in_progress_tasks: int = 0

    completed_tasks: int = 0
    cancelled_tasks: int = 0

    paused_tasks: int = 0
    scheduled_tasks: int = 0
    delegated_tasks: int = 0
    info_tasks: int = 0

    overdue_tasks: int = 0

    scored_tasks: int = 0
    unscored_tasks: int = 0

    total_score: int = 0

    score_distribution: dict[str, int] = field(
        default_factory=lambda: {
            "21-25": 0,
            "16-20": 0,
            "11-15": 0,
            "6-10": 0,
            "1-5": 0,
            "0": 0,
            "no_score": 0,
        }
    )

@dataclass(slots=True)
class SectionMetrics:
    section: Section

    total_tasks: int = 0

    active_tasks: int = 0
    actionable_tasks: int = 0

    completed_tasks: int = 0
    cancelled_tasks: int = 0

    scored_tasks: int = 0
    total_score: int = 0

    wip_limit: int | None = None

    @property
    def average_score(self) -> float:
        if self.scored_tasks == 0:
            return 0.0

        return self.total_score / self.scored_tasks

    @property
    def wip_usage(self) -> float | None:
        if self.wip_limit is None:
            return None

        if self.wip_limit == 0:
            return 0.0

        return self.active_tasks / self.wip_limit


    
@dataclass(slots=True)
class WipMetrics:
    wip_count: int
    wip_limit_exceeded: bool
    
@dataclass(slots=True)
class AnalyticsSnapshot:
    board: BoardMetrics
    sections: Mapping[str, SectionMetrics]