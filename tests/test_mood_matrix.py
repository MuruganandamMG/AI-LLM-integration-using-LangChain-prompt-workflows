from app.services.mood_matrix_service import MoodMatrixService

def test_empty_mood_logs():
    res = MoodMatrixService.calculate_mood_impact([])
    assert res["average_mood"] == 0.0

def test_mood_calculation():
    logs = [
        {"habit_title": "Run", "mood_score": 5},
        {"habit_title": "Read", "mood_score": 3}
    ]
    res = MoodMatrixService.calculate_mood_impact(logs)
    assert res["average_mood"] == 4.0
    assert "Run" in res["high_mood_habits"]
