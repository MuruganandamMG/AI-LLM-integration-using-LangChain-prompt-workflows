import json
from langchain_core.output_parsers import JsonOutputParser
from app.ai.factory import LLMFactory
from app.ai.prompts import PRODUCTIVITY_ANALYTICS_PROMPT
from app.config import settings

async def run_productivity_analytics_chain(user_name: str, stats: dict) -> dict:
    llm = LLMFactory.get_llm()
    stats_summary = f"Total Habits: {stats.get('total_habits', 0)}, Completion Rate: {stats.get('completion_rate', 0)}%, Longest Streak: {stats.get('streak', 0)} days."
    
    if llm is None:
        return {
            "ai_summary": f"{user_name} shows steady habit consistency with a completion rate of {stats.get('completion_rate', 0)}%. Keep protecting momentum during peak productivity windows.",
            "key_takeaways": [
                f"Maintained an active streak of {stats.get('streak', 0)} days.",
                "Completion rate indicates strong dedication across active routines.",
                "Consider increasing habit challenge level gradually."
            ],
            "provider": "mock"
        }
        
    chain = PRODUCTIVITY_ANALYTICS_PROMPT | llm | JsonOutputParser()
    try:
        response = await chain.ainvoke({"user_name": user_name, "stats_summary": stats_summary})
        return response
    except Exception:
        return {
            "ai_summary": f"Performance evaluation completed for {user_name}. Focus on building sustainable habit loops.",
            "key_takeaways": ["Maintain consistency", "Review habit difficulty"],
            "provider": "fallback"
        }
