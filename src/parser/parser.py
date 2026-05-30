from pathlib import Path

from src.parser.metadata import (
    extract_due_date,
    extract_metadata,
    extract_status,
    extract_tags,
    strip_metadata,
)

from src.parser.models import (
    Section,
    Task,
    TaskStatus,
)

from src.parser.sections import (
    resolve_section_type,
)

from src.parser.section_parser import build_section

DEFAULT_SECTION = build_section(
    "Inbox",
    resolve_section_type("Inbox"),
)


from datetime import timedelta

def parse_time_estimate(
    value: str | None,
) -> timedelta | None:
    if value is None:
        return None

    hours = int(value)

    return timedelta(hours=hours)

    

def parse_task_line(
    text: str,
    section: Section,
) -> Task | None:
    """
    Parse a single markdown task line into a Task object.
    """

    status_raw = extract_status(text)

    # Ignore non-task lines
    if status_raw is None:
        return None

    title = strip_metadata(text)

    metadata = extract_metadata(text)

    tags = extract_tags(text)

    due_date = extract_due_date(text)

    score: int | None = None

    if "score" in metadata:
        try:
            score = int(metadata["score"])
        except ValueError:
            score = None

    time_estimate = parse_time_estimate(metadata.get("time"))


    return Task(
        title=title,
        status=TaskStatus(status_raw),

        section=section,

        score=score,
        due=due_date,
        scheduled=None,

        completed_at=None,

        time_estimate=time_estimate,

        tags=tags,
        metadata=metadata,

        archived=False,
        ignored=False,

        updated_at=None,

        raw_line=text,
    )   


def is_section_header(line: str) -> bool:
    """
    Detect markdown section headers.

    Example:
        # Inbox
        ## Today
    """

    stripped = line.strip()

    return stripped.startswith("#")


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


def parse_markdown_file(path: Path) -> list[Task]:
    """
    Parse a markdown file into Task objects.
    """

    text = path.read_text(
        encoding="utf-8"
    )

    lines = text.splitlines()

    return parse_markdown_lines(lines)