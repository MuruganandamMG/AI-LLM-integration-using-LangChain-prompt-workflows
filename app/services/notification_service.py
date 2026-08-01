class NotificationService:
    @staticmethod
    def format_reminder(user_name: str, habit_title: str, streak: int) -> dict:
        return {
            "subject": f"Time for {habit_title}! Keep your {streak}-day streak alive",
            "recipient": user_name,
            "habit": habit_title,
            "streak": streak
        }
