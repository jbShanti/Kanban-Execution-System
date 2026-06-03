from dataclasses import dataclass, field
from src.parser.models import Board, Section, Task
from typing import Mapping
from datetime import datetime



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
class SectionSummary:
    total_tasks: int = 0

    active_tasks: int = 0
    actionable_tasks: int = 0

    completed_tasks: int = 0
    cancelled_tasks: int = 0

    scored_tasks: int = 0
    total_score: int = 0

    @property
    def average_score(self) -> float:
        if self.scored_tasks == 0:
            return 0.0

        return self.total_score / self.scored_tasks


@dataclass(slots=True)
class SectionMetrics:
    section: Section
    summary: SectionSummary

    wip_limit: int | None = None

    @property
    def total_tasks(self) -> int:
        return self.summary.total_tasks

    @property
    def active_tasks(self) -> int:
        return self.summary.active_tasks

    @property
    def actionable_tasks(self) -> int:
        return self.summary.actionable_tasks

    @property
    def completed_tasks(self) -> int:
        return self.summary.completed_tasks

    @property
    def cancelled_tasks(self) -> int:
        return self.summary.cancelled_tasks

    @property
    def scored_tasks(self) -> int:
        return self.summary.scored_tasks

    @property
    def total_score(self) -> int:
        return self.summary.total_score

    @property
    def average_score(self) -> float:
        return self.summary.average_score

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
class WipStatus:
    section_name: str

    active_tasks: int
    wip_limit: int

    remaining_capacity: int
    utilization: float

    is_near_limit: bool
    is_over_limit: bool
    
@dataclass(slots=True, frozen=True)
class StaleTask:
    task: Task

    age_days: int

    is_stale: bool
    is_critical: bool

    last_updated: datetime
    
    

@dataclass(slots=True, frozen=True)
class PriorityScore:
    task: Task

    base_score: int
    section_bonus: int

    final_score: int

    
@dataclass(slots=True, frozen=True)
class AttentionScore:
    task: Task

    stale_score: int
    due_score: int

    final_score: float
    

@dataclass(slots=True, frozen=True)
class HealthWarning:
    category: str
    message: str


@dataclass(slots=True, frozen=True)
class BoardHealthReport:
    board_health_score: float

    wip_violations: int
    stale_task_count: int

    top_priority_tasks: list[PriorityScore]
    top_attention_tasks: list[AttentionScore]

    warnings: list[HealthWarning] 
    
@dataclass(slots=True, frozen=True)
class TaskMetrics:
    active_tasks: int = 0
    completed_tasks: int = 0
    cancelled_tasks: int = 0
    delegated_tasks: int = 0
    scheduled_tasks: int = 0
    archived_tasks: int = 0
    overdue_tasks: int = 0
    
    due_today_tasks: int = 0   
    due_next_3_days_tasks: int = 0
    tasks_without_score: int = 0

    total_score: int = 0
    active_score: int = 0
    
# analytics/models.py

def empty_distribution() -> dict[str, int]:
    return {
        "21-25": 0,
        "16-20": 0,
        "11-15": 0,
        "6-10": 0,
        "1-5": 0,
        "0": 0,
        "no_score": 0,
    }




def empty_statuses() -> dict[str, int]:
    return {}


def empty_sections() -> dict[str, SectionSummary]:
    return {}


@dataclass(slots=True)
class BoardSummary:
    total_tasks: int = 0

    active_tasks: int = 0
    actionable_tasks: int = 0

    completed_tasks: int = 0
    cancelled_tasks: int = 0

    overdue_tasks: int = 0

    scored_tasks: int = 0
    unscored_tasks: int = 0

    total_score: int = 0

    score_distribution: dict[str, int] = field(
        default_factory=empty_distribution
    )

    by_status: dict[str, int] = field(
        default_factory=empty_statuses
    )

    sections: dict[str, SectionSummary] = field(
        default_factory=empty_sections
    )

    @property
    def average_score(self) -> float:
        if self.scored_tasks == 0:
            return 0.0

        return self.total_score / self.scored_tasks
    
@dataclass(slots=True)
class AnalyticsSnapshot:
    summary: BoardSummary
    board: BoardMetrics
    sections: Mapping[str, SectionMetrics]
    
    
@dataclass(slots=True)
class AnalyticsContext:
    board: Board
    summary: BoardSummary
    