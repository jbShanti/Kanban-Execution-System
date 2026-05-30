from src.analytics.priority_scoring import (
    calculate_priority_scores,
)
from src.parser.models import (
    Section,
    SectionType,
    Task,
    TaskStatus,
)


def test_calculates_priority_scores():
    strategic = Section(
        title="Strategic",
        raw_title="Strategic",
        type=SectionType.STRATEGIC,
        priority_weight=5,
    )

    focus = Section(
        title="Focus",
        raw_title="Focus",
        type=SectionType.FOCUS,
        priority_weight=2,
    )

    tasks = [
        Task(
            title="High value",
            status=TaskStatus.OPEN,
            section=strategic,
            score=15,
        ),
        Task(
            title="Medium value",
            status=TaskStatus.IN_PROGRESS,
            section=focus,
            score=10,
        ),
        Task(
            title="Completed",
            status=TaskStatus.COMPLETED,
            section=strategic,
            score=25,
        ),
    ]

    results = calculate_priority_scores(tasks)

    assert len(results) == 2

    highest = results[0]

    assert highest.task.title == "High value"
    assert highest.base_score == 15
    assert highest.section_bonus == 5
    assert highest.final_score == 20

    second = results[1]

    assert second.task.title == "Medium value"
    assert second.base_score == 10
    assert second.section_bonus == 2
    assert second.final_score == 12
    
    
from src.analytics.priority_scoring import (
    calculate_priority_scores,
)
from src.parser.models import (
    Section,
    SectionType,
    Task,
    TaskStatus,
)


def test_uses_zero_when_score_missing():
    section = Section(
        title="Focus",
        raw_title="Focus",
        type=SectionType.FOCUS,
        priority_weight=3,
    )

    task = Task(
        title="Unscored",
        status=TaskStatus.OPEN,
        section=section,
        score=None,
    )

    results = calculate_priority_scores([task])

    assert len(results) == 1

    priority = results[0]

    assert priority.base_score == 0
    assert priority.section_bonus == 3
    assert priority.final_score == 3
    
def test_ignores_non_actionable_tasks():
    section = Section(
        title="Focus",
        raw_title="Focus",
        type=SectionType.FOCUS,
        priority_weight=3,
    )

    tasks = [
        Task(
            title="Open",
            status=TaskStatus.OPEN,
            section=section,
            score=5,
        ),
        Task(
            title="Completed",
            status=TaskStatus.COMPLETED,
            section=section,
            score=10,
        ),
    ]

    results = calculate_priority_scores(tasks)

    assert len(results) == 1

    priority = results[0]

    assert priority.task.title == "Open"
    
def test_returns_empty_list_when_no_actionable_tasks():
    section = Section(
        title="Focus",
        raw_title="Focus",
        type=SectionType.FOCUS,
        priority_weight=3,
    )

    tasks = [
        Task(
            title="Completed",
            status=TaskStatus.COMPLETED,
            section=section,
            score=10,
        ),
        Task(
            title="Cancelled",
            status=TaskStatus.CANCELLED,
            section=section,
            score=5,
        ),
    ]

    results = calculate_priority_scores(tasks)

    assert len(results) == 0