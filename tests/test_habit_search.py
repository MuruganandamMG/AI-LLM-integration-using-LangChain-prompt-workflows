import pytest
from app.schemas.habit_filter import HabitFilterParams

def test_habit_filter_defaults():
    params = HabitFilterParams()
    assert params.category is None
    assert params.search is None

def test_habit_filter_with_values():
    params = HabitFilterParams(category="Fitness", search="morning")
    assert params.category == "Fitness"
    assert params.search == "morning"
