from datetime import date
from src.parser.models import Task


def calculate_high_five(tasks: list[Task]) -> list[Task]:
    """
    Select top 5 tasks for the day based on:
    1. Status (active tasks first)
    2. Score (higher first)
    3. Due date (closer/overdue first)
    """
    # First sort by due date ascending (earliest first).
    # Use a very far date for None.
    tasks_sorted = sorted(tasks, key=lambda t: t.due if t.due is not None else date(9999, 12, 31))
    
    # Then sort by score descending (highest first)
    tasks_sorted = sorted(tasks_sorted, key=lambda t: t.score if t.score is not None else -1, reverse=True)
    
    # Finally sort by active status descending (True first)
    tasks_sorted = sorted(tasks_sorted, key=lambda t: t.is_active, reverse=True)
    
    return tasks_sorted[:5]
