from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from app.ai.factory import LLMFactory

COACH_CHAT_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are Aura, an elite, empathetic, and scientifically-grounded AI Personal Growth and Habit Coach.
Your goal is to help {user_name} build high-leverage habits, overcome procrastination, optimize focus, and cultivate iron consistency.

User Context:
- Active Habits: {habits_context}
- Active Streak: {streak_days} days
- Level & XP: Level {level} ({total_xp} XP)

Guidelines:
1. Provide actionable, concise, and structured advice (use bullet points or numbered steps where helpful).
2. Balance deep empathy with practical accountability.
3. Suggest psychological tools (e.g. implementation intentions, habit stacking, 2-minute rule, friction reduction).
4. Keep answers motivating, punchy, and clear."""),
    ("user", "{message}")
])

async def run_coach_chat_chain(
    user_name: str,
    message: str,
    habits_context: str = "No habits registered yet",
    streak_days: int = 0,
    level: int = 1,
    total_xp: int = 0
) -> dict:
    llm = LLMFactory.get_llm()
    if llm is None:
        # Intelligent contextual fallback responses
        lower_msg = message.lower()
        if "procrastinat" in lower_msg or "start" in lower_msg or "delay" in lower_msg:
            reply = f"Hey {user_name}! Procrastination is usually an emotional regulation issue rather than a time management problem. Here is a 3-step action plan to break through right now:\n\n1. **The 2-Minute Gateway**: Commit to only doing 120 seconds of the task. Lower the activation energy so low that your brain cannot refuse.\n2. **Identify the Hidden Friction**: Are you unclear on the first step? Open the document, write 1 sentence, or set up your tools.\n3. **Habit Stacking**: Attach this task to something you already do effortlessly (e.g., *'After I brew morning coffee, I will immediately open my workspace'*).\n\nYou're currently on a **{streak_days}-day streak**—let's keep the momentum alive!"
        elif "morning" in lower_msg or "wake" in lower_msg or "early" in lower_msg:
            reply = f"Great question, {user_name}! Building an early morning routine comes down to **evening priming and morning light exposure**:\n\n1. **Light Exposure within 10 mins**: Step outside or look near a bright window immediately upon waking to trigger your cortisol awakening response and reset your circadian clock.\n2. **No High-Dopamine Traps**: Keep your phone outside arm's reach. Don't scroll social media or email in the first 30 minutes.\n3. **Prepare the Night Before**: Lay out your workout gear or open your reading material the night before to eliminate morning decision fatigue.\n\nStart small: shift your alarm by just 15 minutes earlier every 3 days rather than 2 hours at once!"
        elif "focus" in lower_msg or "distract" in lower_msg or "timer" in lower_msg:
            reply = f"To achieve deep flow state for your sessions, {user_name}:\n\n- **Use the Focus Mode tab**: Run a 25-minute Pomodoro block with Binaural 40Hz or Brown noise to dampen background distractions.\n- **The Scratchpad Technique**: Whenever an unrelated urge pops up (checking messages, searching a random question), jot it on paper and immediately return to the task.\n- **Single-Tasking Rule**: Close all unrelated tabs and notifications. Multi-tasking degrades cognitive throughput by up to 40%."
        elif "review" in lower_msg or "habit" in lower_msg or "suggest" in lower_msg:
            reply = f"Looking at your active routine:\n**Current Habits:** {habits_context}\n\n**Coaching Recommendation:**\n- Ensure you have a clear balance across **Mindfulness, Physical Energy, and High-Leverage Productivity**.\n- Remember: *'Never miss twice.'* If an unexpected event disrupts a day, log a 2-minute micro-version to protect the identity of consistency.\n- Keep logging your daily mood after completions so we can identify which habits give you the highest energy return!"
        else:
            reply = f"Hello {user_name}! As your Aura growth coach, I'm here to support your consistency and focus. You are currently **Level {level} with {total_xp} XP** and a **{streak_days}-day streak**.\n\nHow can I help you today? You can ask me for routine optimizations, habit stacking ideas, unblocking procrastination, or designing a personalized study/work schedule!"
            
        return {
            "response": reply,
            "provider": "mock",
            "user_name": user_name
        }

    chain = COACH_CHAT_PROMPT | llm | StrOutputParser()
    try:
        response_text = await chain.ainvoke({
            "user_name": user_name,
            "message": message,
            "habits_context": habits_context,
            "streak_days": streak_days,
            "level": level,
            "total_xp": total_xp
        })
        return {
            "response": response_text,
            "provider": "llm",
            "user_name": user_name
        }
    except Exception as e:
        return {
            "response": f"I'm here with you, {user_name}! Focus on keeping your daily streak active and taking the next smallest actionable step today.",
            "provider": "fallback",
            "user_name": user_name
        }
