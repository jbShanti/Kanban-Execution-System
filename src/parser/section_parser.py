import re
from typing import Optional

from src.parser.models import Section, SectionType


PRIORITY_PATTERN = re.compile(
    r"\[P::(?P<priority>[0-5])\]",
)

WIP_PATTERN = re.compile(
    r"\((?P<wip>\d+)\)",
)


def extract_priority_weight(
    raw_title: str,
) -> Optional[int]:
    match = PRIORITY_PATTERN.search(raw_title)

    if match is None:
        return None

    return int(match.group("priority"))


def extract_wip_limit(
    raw_title: str,
) -> Optional[int]:
    match = WIP_PATTERN.search(raw_title)

    if match is None:
        return None

    return int(match.group("wip"))


def clean_section_title(
    raw_title: str,
) -> str:
    title = PRIORITY_PATTERN.sub("", raw_title)
    title = WIP_PATTERN.sub("", title)

    return title.strip()


def build_section(
    raw_title: str,
    section_type: SectionType,
) -> Section:
    return Section(
        title=clean_section_title(raw_title),
        raw_title=raw_title,
        type=section_type,
        wip_limit=extract_wip_limit(raw_title),
        priority_weight=extract_priority_weight(raw_title),
    )