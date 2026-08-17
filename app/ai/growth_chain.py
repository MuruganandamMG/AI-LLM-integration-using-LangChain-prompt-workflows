import json
from langchain_core.output_parsers import JsonOutputParser
from app.ai.factory import LLMFactory
from app.ai.prompts import GROWTH_RECOMMENDATION_PROMPT
from app.config import settings

async def run_growth_recommendation_chain(user_name: str, habits: list[dict]) -> dict:
    llm = LLMFactory.get_llm()
    habits_summary = "\n".join([f"- {h['title']} ({h['category']}): {h.get('logs_count', 0)} completions" for h in habits]) or "No active habits logged yet."
    
    if llm is None:
        # Mock structured response for local development when no API keys are configured
        return {
            "title": "Optimize Daily Focus & Momentum",
            "category": "Productivity",
            "action_items": [
                "Schedule a 25-minute deep work block every morning.",
                "Log mood scores after habit completions to identify optimal productivity hours.",
                "Maintain habit streaks by starting with small, achievable micro-habits."
            ],
            "reasoning": "Consistent small wins establish momentum and protect against cognitive fatigue.",
            "provider": "mock"
        }
        
    chain = GROWTH_RECOMMENDATION_PROMPT | llm | JsonOutputParser()
    try:
        response = await chain.ainvoke({"user_name": user_name, "habits_summary": habits_summary})
        response["provider"] = settings.DEFAULT_LLM_PROVIDER
        return response
    except Exception:
        return {
            "title": "Establish Consistency & Routine",
            "category": "Mindfulness",
            "action_items": ["Set a fixed daily reminder", "Track weekly progress summaries"],
            "reasoning": "Fallback recommendation generated due to LLM response parser format.",
            "provider": "fallback"
        }
