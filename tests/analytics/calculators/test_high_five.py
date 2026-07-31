import pytest
from datetime import date
from src.parser.models import Task, TaskStatus, Section, SectionType
from src.analytics.calculators.high_five import calculate_high_five


def create_task(title: str, status: TaskStatus, score: int | None = None, due: date | None = None) -> Task:
    section = Section(title="Test", raw_title="Test", type=SectionType.TACTICAL)
    return Task(
        title=title,
        status=status,
        section=section,
        score=score,
        due=due
    )


def test_high_five_selects_top_5():
    tasks = [
        create_task(f"Task {i}", TaskStatus.OPEN, score=i)
        for i in range(10)
    ]
    
    result = calculate_high_five(tasks)
    
    assert len(result) == 5
    # Should pick tasks with scores 9, 8, 7, 6, 5
    assert result[0].title == "Task 9"
    assert result[-1].title == "Task 5"


def test_high_five_prioritizes_score_then_due_date():
    t1 = create_task("High Score", TaskStatus.OPEN, score=20, due=date(2026, 1, 10))
    t2 = create_task("Lower Score Soon", TaskStatus.OPEN, score=10, due=date(2026, 1, 1))
    t3 = create_task("Same Score Later", TaskStatus.OPEN, score=20, due=date(2026, 1, 15))
    
    tasks = [t2, t3, t1]
    result = calculate_high_five(tasks)
    
    # Priority 1: Score (t1, t3 have 20)
    # Priority 2: Due date (t1: Jan 10, t3: Jan 15)
    assert result[0].title == "High Score"
    assert result[1].title == "Same Score Later"
    assert result[2].title == "Lower Score Soon"


def test_high_five_prioritizes_active_tasks():
    active = create_task("Active", TaskStatus.OPEN, score=10)
    completed = create_task("Completed", TaskStatus.COMPLETED, score=100)
    
    tasks = [completed, active]
    result = calculate_high_five(tasks)
    
    # Even though completed has much higher score, active should come first
    assert result[0].title == "Active"
    assert result[1].title == "Completed"


def test_high_five_handles_missing_data():
    t1 = create_task("No Score", TaskStatus.OPEN, score=None)
    t2 = create_task("With Score", TaskStatus.OPEN, score=5)
    
    result = calculate_high_five([t1, t2])
    assert result[0].title == "With Score"
    assert result[1].title == "No Score"


def test_high_five_handles_fewer_than_5_tasks():
    tasks = [create_task("Only One", TaskStatus.OPEN, score=10)]
    result = calculate_high_five(tasks)
    assert len(result) == 1
    assert result[0].title == "Only One"
