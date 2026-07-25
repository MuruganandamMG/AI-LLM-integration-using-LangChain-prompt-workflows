from app.schemas.quest import DailyQuest

class QuestService:
    @staticmethod
    def get_daily_quests(completed_logs_count: int) -> list[DailyQuest]:
        return [
            DailyQuest(id="q1", title="Complete at least 1 habit today", xp_reward=50, is_completed=completed_logs_count >= 1),
            DailyQuest(id="q2", title="Complete 3 habits in a single day", xp_reward=150, is_completed=completed_logs_count >= 3),
            DailyQuest(id="q3", title="Log your mood score after habit completion", xp_reward=75, is_completed=completed_logs_count >= 1)
        ]
