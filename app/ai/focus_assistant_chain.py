from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from app.ai.factory import LLMFactory

FOCUS_PROMPT = ChatPromptTemplate.from_messages([
    ("system", "You are a deep-work and flow-state AI assistant. Given a task and duration, produce 3 priming steps, an anti-distraction tip, and a focus countdown soundtrack suggestion in JSON format with keys: 'priming_steps', 'anti_distraction_tip', 'music_suggestion'."),
    ("user", "Task: {task_title}\nDuration: {duration_minutes} minutes\n\nPrepare focus session strategy.")
])

async def run_focus_assistant_chain(task_title: str, duration_minutes: int = 25) -> dict:
    llm = LLMFactory.get_llm()
    if llm is None:
        return {
            "priming_steps": [
                "Clear browser tabs except the current working document",
                "Place smartphone in another room or turn on Do Not Disturb",
                "Take 3 deep box-breaths before typing"
            ],
            "anti_distraction_tip": "If an unrelated thought arises, jot it down on paper and return to work.",
            "music_suggestion": "Binaural beats 40Hz (Gamma waves for peak concentration)",
            "provider": "mock"
        }
    chain = FOCUS_PROMPT | llm | JsonOutputParser()
    try:
        return await chain.ainvoke({"task_title": task_title, "duration_minutes": duration_minutes})
    except Exception:
        return {
            "priming_steps": ["Close distractions", "Set timer"],
            "anti_distraction_tip": "Focus on one item at a time.",
            "music_suggestion": "Lo-Fi Instrumental",
            "provider": "fallback"
        }
