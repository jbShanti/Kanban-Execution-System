import re
from datetime import date
from typing import Final


METADATA_PATTERN: Final = re.compile(
    r"\[([a-z0-9\-]+)::([^\]]+)\]"
)

TAG_PATTERN: Final = re.compile(
    r"#([\w/\-]+)",
    re.UNICODE,
)

DUE_PATTERN: Final = re.compile(
    r"@\{(\d{4}-\d{2}-\d{2})\}"
)

WHITESPACE_PATTERN: Final = re.compile(r"\s+")

STATUS_PATTERN: Final = re.compile(
    r"^\s*-\s\[([ x/\-<>i])\]"
)

STATUS_MAP: Final[dict[str, str]] = {
    " ": "open",
    "x": "completed",
    "/": "in_progress",
    "-": "cancelled",
    "<": "scheduled",
    ">": "delegated",
    "i": "info",
}

STATUS_CLEAN_PATTERN: Final = re.compile(
    r"^\s*-\s\[[ x/\-<>i]\]\s*"
)

INTERNAL_LINK_PATTERN: Final = re.compile(
    r"\[\[([^\|\]]+)(?:\|([^\]]+))?\]\]"
)

EXTERNAL_LINK_PATTERN: Final = re.compile(
    r"\[([^\]]+)\]\(([^)]+)\)"
)

def extract_metadata(text: str) -> dict[str, str]:
    metadata: dict[str, str] = {}

    matches = METADATA_PATTERN.findall(text)

    for key, value in matches:
        if key not in metadata:
            metadata[key] = value.strip()

    return metadata

def extract_tags(text: str) -> list[str]:
    return TAG_PATTERN.findall(text)

def extract_due_date(text: str) -> date | None:
    match = DUE_PATTERN.search(text)

    if not match:
        return None

    try:
        return date.fromisoformat(match.group(1))
    except ValueError:
        return None

def extract_internal_links(text: str) -> list[tuple[str, str]]:
    return INTERNAL_LINK_PATTERN.findall(text)

def extract_external_links(text: str) -> list[tuple[str, str]]:
    return EXTERNAL_LINK_PATTERN.findall(text)

def extract_status(text: str) -> str | None:
    match = STATUS_PATTERN.search(text)

    if not match:
        return None

    raw_status = match.group(1)

    return STATUS_MAP.get(raw_status)

def normalize_whitespace(text: str) -> str:
    return WHITESPACE_PATTERN.sub(" ", text).strip()

def strip_metadata(text: str) -> str:
    text = METADATA_PATTERN.sub("", text)
    text = TAG_PATTERN.sub("", text)
    text = DUE_PATTERN.sub("", text)

    text = INTERNAL_LINK_PATTERN.sub(r"\1", text)
    text = EXTERNAL_LINK_PATTERN.sub(r"\1", text)

    text = STATUS_CLEAN_PATTERN.sub("", text)

    return normalize_whitespace(text)