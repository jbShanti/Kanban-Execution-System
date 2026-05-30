from enum import Enum
from datetime import date, datetime
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

    time_estimate: str | None = None

    tags: list[str] = field(
        default_factory=lambda: [],
    )

    metadata: dict[str, str] = field(
       default_factory=lambda: {},
    )

    archived: bool = False
    ignored: bool = False

    raw_line: str = ""
    
    
    @property
    def is_completed(self) -> bool:
        return self.status == TaskStatus.COMPLETED

    @property
    def is_open(self) -> bool:
        return self.status in {
            TaskStatus.OPEN,
            TaskStatus.IN_PROGRESS,
            TaskStatus.SCHEDULED,
            TaskStatus.PAUSED,
        }
