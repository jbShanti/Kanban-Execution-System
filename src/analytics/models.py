from __future__ import annotations  # ✅ Решает forward references

from enum import StrEnum
from dataclasses import dataclass, field
from src.parser.models import Board, Section, Task, TaskStatus
from datetime import datetime, date

from typing import Mapping


SCORE_CORRIDOR_ORDER = (
    "21-25",
    "16-20",
    "11-15",
    "6-10",
    "1-5",
    "0",
    "no_score",
)


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



@dataclass(slots=True)
class SectionSummary:
    total_tasks: int = 0

    active_tasks: int = 0
    actionable_tasks: int = 0

    completed_tasks: int = 0
    cancelled_tasks: int = 0

    scored_tasks: int = 0
    total_score: int = 0
    
    def __hash__(self) -> int:
        """Make SectionSummary hashable for use in frozenset/dict.
        
        All fields are primitive ints, so hash is stable and fast.
        """
        return hash((
            self.total_tasks,
            self.active_tasks,
            self.actionable_tasks,
            self.completed_tasks,
            self.cancelled_tasks,
            self.scored_tasks,
            self.total_score,
        ))

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


@dataclass(slots=True)
class OverloadSignal:
    """Represents a workload overload warning for a specific section."""
    section_name: str
    severity: str  # "WARNING" (near limit) or "CRITICAL" (over limit)
    message: str


class MissingMetadata(StrEnum):
    SCORE = "score"
    TAG = "tag"
    
    
@dataclass(frozen=True)
class OrphanTask:
    title: str
    is_active: bool
    missing: tuple[MissingMetadata, ...]
    
    
class BoardHealthStatus(StrEnum):
    EXCELLENT = "excellent"
    GOOD = "good"
    WARNING = "warning"
    POOR = "poor"
    AWFUL = "awful"
    CRITICAL = "critical"


@dataclass(frozen=True)
class BoardHealth:
    total_tasks: int
    active_tasks: int

    score_coverage: float
    tag_coverage: float
    analytics_coverage: float

    missing_score: int
    missing_tag: int

    orphan_tasks: int

    sample_orphans: tuple[OrphanTask,...]

    status: BoardHealthStatus


@dataclass(frozen=True)
class ExecutiveSummary:
    summary: str


   
    
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
class ScoreCorridorSummary:
    task_count: int = 0

    scored_tasks: int = 0

    total_score: int = 0
    
    def __hash__(self) -> int:
        """Make ScoreCorridorSummary hashable for use in frozenset/dict."""
        return hash((
            self.task_count,
            self.scored_tasks,
            self.total_score,
            # Добавь другие примитивные поля, если они есть в классе
        ))
    
    
    @property
    def average_score(self) -> float:
        if self.scored_tasks == 0:
            return 0.0

        return self.total_score / self.scored_tasks
    
    def percentage_of(
        self,
        total_tasks: int,
    ) -> float:
        if total_tasks == 0:
            return 0.0

        return (
            self.task_count
            / total_tasks
            * 100
        )
    
def empty_score_corridors() -> dict[str, ScoreCorridorSummary]:
    return {
        "21-25": ScoreCorridorSummary(),
        "16-20": ScoreCorridorSummary(),
        "11-15": ScoreCorridorSummary(),
        "6-10": ScoreCorridorSummary(),
        "1-5": ScoreCorridorSummary(),
        "0": ScoreCorridorSummary(),
        "no_score": ScoreCorridorSummary(),
    }

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


    score_corridors: dict[str, ScoreCorridorSummary] = field(
    default_factory=empty_score_corridors,
)
    by_status: dict[str, int] = field(
        default_factory=empty_statuses
    )

    sections: dict[str, SectionSummary] = field(
        default_factory=empty_sections
    )

    def __hash__(self) -> int:
        """Custom hash to make BoardSummary hashable despite dict fields.
    
        Converts dict fields to frozenset of tuples for hashability.
        """
        return hash((
            self.total_tasks,
            frozenset(self.by_status.items()),
            frozenset(self.sections.items()),
            frozenset(self.score_corridors.items()),
        ))
        
    @property
    def average_score(self) -> float:
        if self.scored_tasks == 0:
            return 0.0

        return self.total_score / self.scored_tasks
    

    
@dataclass(slots=True)
class AnalyticsContext:
    board: Board
    summary: BoardSummary
    
@dataclass(slots=True, frozen=True)
class ScoreCorridor:
    name: str

    task_count: int

    total_score: int
    average_score: float

    percentage: float
    score_share_percentage: float
    
   
    
@dataclass(frozen=True)
class AnalyticsTaskSnapshot:
    title: str

    section: str
    status: TaskStatus

    score: int | None
    
    tags: tuple[str, ...]
    
    due_date: date | None
    scheduled_date: date | None

    time_estimate_minutes: int | None

    
    is_active: bool
    is_completed: bool
    is_archived: bool
    is_overdue: bool
    
    category: str | None = None
    cost: int | None = None
    currency: str | None = None
    analytics_ignore: bool = False 
    
    
@dataclass(frozen=True)
class FocusAttentionAnalytics:
    active_tasks: int
    overdue_tasks: int
    high_score_tasks: int

    attention_by_tag: dict[str, int]
    
    total_attention_score: int
    top_attention_tags: tuple[
       tuple[str, int, float],
       ...
    ]
    
from datetime import date, datetime
from dataclasses import dataclass

# ... другие импорты ...

@dataclass(frozen=True)
class ExecutionReport:
    """
    Canonical immutable snapshot of the execution system state.
    
    ExecutionReport is the final output of the analytics pipeline and
    the sole contract consumed by all presentation artifacts.
    """
    # ============================================================
    # 1. METADATA AND PROVENANCE
    # ============================================================
    schema_version: str = "1.0"
    report_id: str = ""
    analysis_date: date = date(1970, 1, 1)
    generated_at: datetime = datetime(1970, 1, 1)
    board_path: str = ""
    
    # ============================================================
    # 2. CORE ANALYTICS
    # ============================================================
    board_health: BoardHealth = None  # type: ignore
    board_summary: BoardSummary = None  # type: ignore  # ← ДОБАВИТЬ
    executive_summary: ExecutiveSummary = None  # type: ignore
        
@dataclass(slots=True)
class AnalyticsSnapshot:
    summary: BoardSummary
    board: BoardMetrics
    sections: Mapping[str, SectionMetrics]
    # ...