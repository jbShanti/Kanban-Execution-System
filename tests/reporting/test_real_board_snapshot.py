import os
from pathlib import Path

from src.parser.models import Section
from src.application.review_service import run_review

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

    # print(snapshot.summary)
    # print(snapshot.board)

    assert snapshot.summary.total_tasks > 0
    assert len(snapshot.sections) > 0


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
    
    
def test_real_board_snapshot_builds_2():
    # 1. Загружаем реальную доску
    board = load_real_board()
    
    # 2. Генерируем отчёт (предполагаем, что функция называется run_review)
    # Если у тебя она называется иначе, замени run_review на нужное имя
    report_markdown = run_review(tasks=board.tasks)
    
    # 3. Базовая проверка: отчёт не пустой
    assert report_markdown
    assert len(report_markdown) > 100
    
       # ==========================================
    # 4. ПРОВЕРКИ: Целевая проверка Board Health
    # ==========================================
    
    # Проверяем, что заголовок секции здоровья присутствует
    assert "Board Health" in report_markdown
    
    # Проверяем, что секция перегрузки отрендерилась
    assert "⚠️ Overload Warnings" in report_markdown
    
    # Проверяем конкретные детали из нашей РЕАЛЬНОЙ доски.
    # Как показал вывод ошибки, перегружена секция '🗓️ TODAY' (4/3)
    assert "🗓️ TODAY" in report_markdown
    assert "OVER WIP limit (4/3 tasks)" in report_markdown
    
    # Проверяем наличие эмодзи-индикатора критической перегрузки
    assert "🔴" in report_markdown
    
    # ==========================================
    # 5. ВЫГРУЗКА ФАЙЛА для визуальной проверки (Debug)
    # ==========================================
    debug_output_path = Path("report_2.md")
    with open(debug_output_path, "w", encoding="utf-8") as f:
        f.write(report_markdown)
        
    print(f"\n✅ Отчёт успешно сгенерирован и сохранён в: {debug_output_path.absolute()}")
    print("💡 Открой этот файл в VS Code и нажми 'Open Preview' (Ctrl+Shift+V), чтобы увидеть результат!")