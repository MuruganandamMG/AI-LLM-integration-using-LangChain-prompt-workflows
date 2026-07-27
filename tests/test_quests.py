from app.services.quest_service import QuestService

def test_daily_quests_completion():
    quests = QuestService.get_daily_quests(completed_logs_count=2)
    assert quests[0].is_completed is True
    assert quests[1].is_completed is False
