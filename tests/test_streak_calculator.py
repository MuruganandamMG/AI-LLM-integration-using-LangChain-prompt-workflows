from datetime import datetime, timezone, timedelta
from app.services.streak_calculator import StreakCalculator

def test_empty_dates_streak():
    assert StreakCalculator.calculate_current_streak([]) == 0

def test_active_streak():
    today = datetime.now(timezone.utc)
    dates = [today, today - timedelta(days=1), today - timedelta(days=2)]
    assert StreakCalculator.calculate_current_streak(dates) == 3

def test_broken_streak():
    today = datetime.now(timezone.utc)
    dates = [today - timedelta(days=5), today - timedelta(days=6)]
    assert StreakCalculator.calculate_current_streak(dates) == 0
