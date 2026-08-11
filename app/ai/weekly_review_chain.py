from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from app.ai.factory import LLMFactory
from app.config import settings

WEEKLY_REVIEW_PROMPT = ChatPromptTemplate.from_messages([
    ("system", "You are an executive personal growth coach. Analyze the user's past 7 days of habit achievements, identify key wins, flag areas for improvement, and generate 3 concrete SMART goals for the coming week in JSON format with keys: 'overall_sentiment', 'wins', 'improvement_areas', 'next_week_smart_goals', 'coach_note'."),
    ("user", "User Profile: {user_name}\nWeekly Performance Data:\n{summary_data}\n\nDeliver the weekly coaching debrief.")
])

async def run_weekly_review_chain(user_name: str, summary_data: dict) -> dict:
    llm = LLMFactory.get_llm()
    
    if llm is None:
        return {
            "overall_sentiment": "High Momentum & Growth",
            "wins": [
                "Maintained 100% adherence on core morning routines",
                "Logged positive mood scores across continuous focus sessions"
            ],
            "improvement_areas": [
                "Avoid late evening workout scheduling to improve sleep hygiene",
                "Set clear boundaries around deep work time blocks"
            ],
            "next_week_smart_goals": [
                "Complete 5 meditation sessions before 9:00 AM",
                "Log at least 3 deep work blocks of 45+ minutes",
                "Review habit tracker progress every Sunday evening"
            ],
            "coach_note": f"Incredible work this week, {user_name}! Momentum is built one day at a time.",
            "provider": "mock"
        }
        
    chain = WEEKLY_REVIEW_PROMPT | llm | JsonOutputParser()
    try:
        response = await chain.ainvoke({"user_name": user_name, "summary_data": str(summary_data)})
        return response
    except Exception:
        return {
            "overall_sentiment": "Steady Progress",
            "wins": ["Consistent habit logging"],
            "improvement_areas": ["Increase daily logging consistency"],
            "next_week_smart_goals": ["Set daily reminders"],
            "coach_note": "Keep up the momentum!",
            "provider": "fallback"
        }
