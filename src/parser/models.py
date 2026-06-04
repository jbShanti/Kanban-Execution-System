from enum import Enum
from datetime import date, datetime, timedelta
from dataclasses import dataclass, field


class TaskStatus(str, Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    PAUSED = "paused"
    INFO = "info"
    SCHEDULED = "scheduled"
    DELEGATED = "delegated"

def empty_tags() -> list[str]:
    return []

def empty_metadata() -> dict[str, str]:
    return {}


class SectionType(str, Enum):
    INBOX = "inbox"

    TACTICAL = "tactical"
    EXECUTION = "execution"

    QUEUED = "queued"
    FOCUS = "focus"

    WAITING = "waiting"
    STRATEGIC = "strategic"

    DONE = "done"
    ARCHIVE = "archive"

    UNKNOWN = "unknown"
    
    INFO = "info"

@dataclass(slots=True, frozen=True)
class Section:
    title: str
    raw_title: str
    type: SectionType

    wip_limit: int | None = None
    priority_weight: int | None = None


@dataclass(slots=True)
class Task:
    title: str
    status: TaskStatus

    section: Section
        
    score: int | None = None
    due: date | None = None
    scheduled: date | None = None
    completed_at: date | None = None

    updated_at: datetime | None = None

    time_estimate: timedelta | None = None

    tags: list[str] = field(default_factory=empty_tags)

    metadata: dict[str, str] = field(default_factory=empty_metadata)

    archived: bool = False
    ignored: bool = False

    raw_line: str = ""
    
    
    @property
    def is_completed(self) -> bool:
        return self.status == TaskStatus.COMPLETED

    @property
    def is_active(self) -> bool:
        return self.status in {
            TaskStatus.OPEN,
            TaskStatus.IN_PROGRESS,
        }
    
    @property
    def is_actionable(self) -> bool:
        return self.status in {
            TaskStatus.OPEN,
            TaskStatus.IN_PROGRESS,
            TaskStatus.SCHEDULED,
            TaskStatus.PAUSED,
            TaskStatus.DELEGATED,
        }
        
    @property
    def is_cancelled(self) -> bool:
        return self.status == TaskStatus.CANCELLED

    @property
    def is_done(self) -> bool:
        return self.status in {
            TaskStatus.COMPLETED,
            TaskStatus.CANCELLED,
        }
    
    @property
    def score_value(self) -> int:
        return self.score or 0



 
  
 
@dataclass(slots=True)
class StaleTask:
    task: Task

    stale_since: date
    days_overdue: int
    
def empty_reasons() -> list[str]:
    return []

@dataclass(slots=True)
class PriorityScore:
    task: Task

    base_score: int
    overdue_bonus: int
    final_score: int

    reasons: list[str] = field(default_factory=empty_reasons)
    
@dataclass(slots=True)
class Board:
    tasks: list[Task]

    created_at: datetime | None = None
    updated_at: datetime | None = None
    
    @property
    def active_task_list(self) -> list[Task]:
        return [t for t in self.tasks if t.is_active]

    @property
    def actionable_task_list(self) -> list[Task]:
        return [t for t in self.tasks if t.is_actionable]
    
    @property
    def completed_task_list(self) -> list[Task]:
        return [
            t
            for t in self.tasks
            if t.is_completed
        ]
    
    @property
    def sections(self) -> list[Section]:
        unique: dict[str, Section] = {}

        for task in self.tasks:
            unique[task.section.title] = task.section

        return list(unique.values())