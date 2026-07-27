from datetime import datetime, timezone, timedelta

class StreakCalculator:
    @staticmethod
    def calculate_current_streak(completed_dates: list[datetime]) -> int:
        if not completed_dates:
            return 0
        sorted_dates = sorted({d.date() for d in completed_dates}, reverse=True)
        today = datetime.now(timezone.utc).date()
        
        # Check if latest completion is today or yesterday
        if sorted_dates[0] < today - timedelta(days=1):
            return 0
            
        streak = 1
        for i in range(len(sorted_dates) - 1):
            if sorted_dates[i] - sorted_dates[i+1] == timedelta(days=1):
                streak += 1
            else:
                break
        return streak
