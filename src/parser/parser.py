from pathlib import Path

from src.parser.metadata import (
    extract_cost,
    extract_currency,
    extract_due_date,
    extract_emoji,
    extract_metadata,
    extract_priority,
    extract_repeat,
    extract_scheduled_date,
    extract_start_date,
    extract_completion_date,
    extract_status,
    extract_tags,
    strip_emoji,
    strip_metadata,
    extract_analytics,
    extract_category,
    extract_finance,
)

from src.parser.models import (
    Section,
    Task,
    TaskStatus,
    Board,
)

from src.parser.sections import (
    resolve_section_type,
)

from src.parser.section_parser import build_section

from datetime import timedelta

import re


DEFAULT_SECTION = build_section(
    "Inbox",
    resolve_section_type("Inbox"),
)




def parse_duration(
    value: str | None,
) -> timedelta | None:
    """
    Parse duration metadata into timedelta.

    Supported formats:
    - 5m
    - 10min
    - 15m
    - 90m
    - 1h
    - 2h
    - 1.5h
    - 1h30m
    """

    if value is None:
        return None

    value = value.strip().lower()

    # 1h30m
    match = re.fullmatch(
        r"(\d+)h(\d+)m",
        value,
    )
    if match:
        hours = int(match.group(1))
        minutes = int(match.group(2))
        return timedelta(
            hours=hours,
            minutes=minutes,
        )

    # 1.5h / 2h
    match = re.fullmatch(
        r"(\d+(?:\.\d+)?)h",
        value,
    )
    if match:
        hours = float(match.group(1))
        return timedelta(hours=hours)

    # 90m / 15m / 10min
    match = re.fullmatch(
        r"(\d+)(?:m|min)",
        value,
    )
    if match:
        minutes = int(match.group(1))
        return timedelta(minutes=minutes)
    
    # 120
    match = re.fullmatch(
        r"(\d+)",
        value,
    )
    if match:
        minutes = int(match.group(1))
        return timedelta(minutes=minutes)

    '''raise ValueError(
        f"Unsupported duration format: {value!r}"
    )
    '''
    
    return None
    

def parse_task_line(
    text: str,
    section: Section,
) -> Task | None:
    """
    Parse a single markdown task line into a Task object.
    """

    depth = extract_depth(text)
    status_raw = extract_status(text)

    # Ignore non-task lines
    if status_raw is None:
        return None

    title = strip_metadata(text)

    emoji: list[str] = []

    if depth == 0:
        emoji = extract_emoji(title)
        title = strip_emoji(title)
    
       
    finance = extract_finance(text)
    
    cost = extract_cost(text)
    
    currency=extract_currency(text)

    tags = extract_tags(text)

    due_date = extract_due_date(text)
    
    scheduled=extract_scheduled_date(text)
    
    start_date = extract_start_date(text)
    
    completion_date = extract_completion_date(text)

    
    priority = extract_priority(text)
    
    analytics=extract_analytics(text)
    
    repeat = extract_repeat(text)
    
    category = extract_category(text)

    score: int | None = None
    
    metadata = extract_metadata(text)

    if "score" in metadata:
        try:
            score = int(metadata["score"])
        except ValueError:
            score = None
    
    time_estimate = parse_duration(metadata.get("time"))
    
    return Task(
        title=title,
        status=TaskStatus(status_raw),

        section=section,

        score=score,
        priority=priority,
        repeat=repeat,
        due=due_date,
        scheduled=scheduled,
        start=start_date,

        completed_at=completion_date,

        time_estimate=time_estimate,

        tags=tags,
        metadata=metadata,
        category=category,
        finance=finance,
        cost=cost,
        currency=currency,
        analytics=analytics,

        archived=False,
        depth=depth,
        emoji=emoji,
        updated_at=None,

        raw_line=text,
    )   


def is_section_header(line: str) -> bool:
    """
    Detect Kanban section headers.

    Example:
        ## Inbox
        ## Today
    """

    return line.startswith("## ")


def extract_section_name(line: str) -> str:
    """
    Extract section name from markdown header.

    Example:
        # Inbox -> Inbox
        ## Today -> Today
    """

    stripped = line.strip()

    return stripped.lstrip("#").strip()


def parse_markdown_lines(
    lines: list[str],
) -> list[Task]:
    """
    Parse markdown lines into Task objects.
    """

    tasks: list[Task] = []

    current_section = DEFAULT_SECTION
    

    for line in lines:

        if is_section_header(line):

            raw_section_title = extract_section_name(line)

            current_section = build_section(
                raw_section_title,
                resolve_section_type(raw_section_title),
            )

            continue

        task = parse_task_line(
            line,
            section=current_section,
        )

        if task is not None:
            tasks.append(task)

    return tasks


from src.parser.models import Board


def parse_markdown_file(
    path: Path,
) -> Board:
    """
    Parse markdown file into Board.
    """

    text = path.read_text(
        encoding="utf-8",
    )

    return Board(parse_markdown_lines(
        text.splitlines()),
    )
    
def extract_depth(
    line: str,
) -> int:
    return len(line) - len(line.lstrip("\t"))