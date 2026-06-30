from src.parser.models import SectionType
from src.parser.parser import parse_markdown_lines


def test_parse_section_with_emoji():
    board = [
        "## 📥 Inbox",
        "- [ ] First task",
    ]

    tasks = parse_markdown_lines(board)

    assert len(tasks) == 1

    section = tasks[0].section

    assert section.raw_title == "📥 Inbox"
    assert section.title == "Inbox"
    assert section.emoji == ["📥"]
    assert section.type == SectionType.INBOX


def test_parse_section_with_priority():
    board = [
        "## ❤️ Health [P::5]",
        "- [ ] Buy vitamins",
    ]

    tasks = parse_markdown_lines(board)

    section = tasks[0].section

    assert section.raw_title == "❤️ Health [P::5]"
    assert section.title == "Health"
    assert section.emoji == ["❤️"]
    assert section.priority_weight == 5


def test_parse_section_with_multiple_metadata():
    board = [
        "## 🚧 Projects [P::4] (3)",
        "- [ ] Implement parser",
    ]

    tasks = parse_markdown_lines(board)

    section = tasks[0].section

    assert section.raw_title == "🚧 Projects [P::4] (3)"
    assert section.title == "Projects"
    assert section.emoji == ["🚧"]
    assert section.priority_weight == 4
    assert section.wip_limit == 3