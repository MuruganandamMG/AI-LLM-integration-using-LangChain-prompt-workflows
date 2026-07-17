class MoodMatrixService:
    @staticmethod
    def calculate_mood_impact(logs: list[dict]) -> dict:
        if not logs:
            return {"average_mood": 0.0, "high_mood_habits": [], "total_rated_logs": 0}
        
        rated_logs = [l for l in logs if l.get("mood_score") is not None]
        if not rated_logs:
            return {"average_mood": 0.0, "high_mood_habits": [], "total_rated_logs": 0}
            
        avg_mood = sum(l["mood_score"] for l in rated_logs) / len(rated_logs)
        high_habits = list({l.get("habit_title", "General") for l in rated_logs if l["mood_score"] >= 4})
        
        return {
            "average_mood": round(avg_mood, 2),
            "high_mood_habits": high_habits,
            "total_rated_logs": len(rated_logs)
        }
