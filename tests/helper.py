from pathlib import Path

from src.parser.models import Board, Section, SectionType, Task, TaskStatus
from src.parser.parser import parse_markdown_file
from src.parser.section_parser import build_section, clean_section_title

from datetime import date, datetime, UTC, timedelta


def load_test_board(
    filename: str | Path,
) -> Board:
    path = Path(filename)

    if not path.is_absolute():
        path = (
            Path("tests/fixtures")
            / path
        )

    return parse_markdown_file(path)

def create_section(
    *,
    title: str = "Inbox",
    section_type: SectionType = SectionType.INBOX,
    emoji: list[str] | None = None,
    priority_weight: int | None = None,
    wip_limit: int | None = None,
) -> Section:
    if emoji is None:
        emoji = []

    raw_title = title

    if emoji:
        raw_title = f"{''.join(emoji)} {raw_title}"

    if priority_weight is not None:
        raw_title += f" [P::{priority_weight}]"

    if wip_limit is not None:
        raw_title += f" ({wip_limit})"

    clean_title = clean_section_title(raw_title)

    return build_section(
        raw_title=raw_title,
        clean_title=clean_title,
        emoji=emoji,
        priority_weight=priority_weight,
        wip_limit=wip_limit,
        section_type=section_type,
    )
    
def create_task(
    *,
    title: str = "Task",
    status: TaskStatus = TaskStatus.OPEN,
    section: Section | None = None,
    section_title: str = "Inbox",
    section_type: SectionType = SectionType.INBOX,
    score: int | None = None,
    due: date | None = None,
    scheduled: date | None = None,
    time_estimate: timedelta | None = None,
    updated_at: datetime | None = None,
    archived: bool = False,
    tags: list[str] | None = None,
    metadata: dict[str, str] | None = None,
    raw_line: str | None = None,
) -> Task:
    if section is None:
        section = create_section(
            title=section_title,
            section_type=section_type,
        )

    if tags is None:
        tags = []

    if metadata is None:
        metadata = {}

    if updated_at is None:
        updated_at = datetime.now(UTC)

    if raw_line is None:
        raw_line = f"- [ ] {title}"

    return Task(
        title=title,
        status=status,
        section=section,
        raw_line=raw_line,
        archived=archived,
        metadata=metadata,
        tags=tags,
        score=score,
        due=due,
        scheduled=scheduled,
        time_estimate=time_estimate,
        updated_at=updated_at,
    )
    

def create_board(
    tasks: list[Task] | None = None,
) -> Board:
    return Board(
        tasks=[] if tasks is None else tasks,
    )