##from typing import Final

from src.parser.models import SectionType


SECTION_ALIASES = {
    "inbox": SectionType.INBOX,

    "today": SectionType.TACTICAL,
    "critical": SectionType.TACTICAL,

    "doing": SectionType.EXECUTION,
    "selected": SectionType.EXECUTION,

    "todo": SectionType.QUEUED,

    "medium priority focus": SectionType.FOCUS,
    "focus": SectionType.FOCUS,

    "waiting": SectionType.WAITING,
    "control, deadlines, await": SectionType.WAITING,

    "goals": SectionType.STRATEGIC,

    "done": SectionType.DONE,
    "archive": SectionType.ARCHIVE,
}

SECTION_PRIORITY_MAP: dict[str, int] = {
    "INBOX": 100,

    "TODAY": 95,

    "DOING": 85,

    "TODO": 70,

    "MEDIUM PRIORITY FOCUS": 60,

    "WAITING": 40,

    "GOALS": 30,
    "UNKNOWN": 30,

    "DONE": 10,
    "ARCHIVE": 0,
}



def normalize_section_name(
    section: str,
) -> str:
    return (
        section
        .strip()
        .lower()
    )


def resolve_section_type(
    section: str,
) -> SectionType:
    normalized = normalize_section_name(
        section
    )
     
    return SECTION_ALIASES.get(
        normalized,
        SectionType.UNKNOWN,
    )