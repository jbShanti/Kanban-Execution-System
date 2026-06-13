import os
from pathlib import Path

from src.parser.models import Section

from src.analytics.service import (
    build_analytics_snapshot,
)

from src.reporting.report_adapter import (
    render_snapshot,
)

from tests.helper import (
    load_test_board,
)


def load_real_board():
    # 1. Проверяем переменную окружения (идеально для CI или других разработчиков)
    env_path = os.getenv("KANBAN_REAL_BOARD_PATH")
    if env_path and Path(env_path).exists():
        return load_test_board(Path(env_path))
    
    # 2. Фоллбэк на твой локальный путь (используем raw-строку r"" или слеши /)
    local_path = Path(r"O:\Проекты\Kanban\Doing (KB).md")
    if local_path.exists():
        return load_test_board(local_path)
    
    # 3. Фоллбэк на стандартный путь в репозитории (если кто-то добавит обезличенный файл)
    repo_path = Path("tests/fixtures/Doing (KB).md")
    if repo_path.exists():
        return load_test_board(repo_path)
        
    raise FileNotFoundError(
        "Не удалось найти файл доски. Установите переменную окружения KANBAN_REAL_BOARD_PATH "
        "или положите файл в O:\\Проекты\\Kanban\\ или tests/fixtures/"
)


def test_real_board_snapshot_builds():
    board = load_real_board()

    snapshot = build_analytics_snapshot(board)

    report = render_snapshot(snapshot)

    print(report)

    report_path = "report.md"

    with open(
        report_path,
        "w",
        encoding="utf-8",
    ) as file:
        file.write(report)

    print(snapshot.summary)
    print(snapshot.board)

    assert snapshot.summary.total_tasks > 0
    assert len(snapshot.sections) > 0


def test_real_board_snapshot_builds_tmp():
    board = load_real_board()

    snapshot = build_analytics_snapshot(board)

    print()

    print(
        "TOTAL:",
        snapshot.summary.total_tasks,
    )

    print(
        "ACTIVE:",
        snapshot.summary.active_tasks,
    )

    print(
        "COMPLETED:",
        snapshot.summary.completed_tasks,
    )

    print(
        "SECTIONS:",
        len(snapshot.sections),
    )

    for (
        name,
        section_summary,
    ) in snapshot.summary.sections.items():
        print(
            name,
            section_summary.total_tasks,
            section_summary.active_tasks,
        )

    assert snapshot.summary.total_tasks > 0


def test_real_board_sections():
    board = load_real_board()

    sections: list[Section] = board.sections

    for section in sections:
        print(
            section.title,
            section.type,
            section.wip_limit,
        )

    assert len(sections) > 0