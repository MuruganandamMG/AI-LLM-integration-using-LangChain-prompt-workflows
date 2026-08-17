import pytest
from scripts.seed_git_history import get_commit_schedule

def test_get_commit_schedule():
    schedule = get_commit_schedule()
    assert len(schedule) >= 6
    assert "msg" in schedule[0]
    assert "days_ago" in schedule[0]
