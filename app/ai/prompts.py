from langchain_core.prompts import ChatPromptTemplate

GROWTH_RECOMMENDATION_PROMPT = ChatPromptTemplate.from_messages([
    ("system", "You are an expert AI performance coach specializing in habit formation, motivation, and goal alignment. Provide structured, practical growth advice in JSON format with keys: 'title', 'category', 'action_items' (list), and 'reasoning'."),
    ("user", "User Profile: {user_name}\nHabits & Log Summary:\n{habits_summary}\n\nGenerate personalized growth recommendations.")
])

PRODUCTIVITY_ANALYTICS_PROMPT = ChatPromptTemplate.from_messages([
    ("system", "You are an AI productivity analyst. Based on habit tracking statistics, analyze consistency, identify burnout risk or positive momentum, and output structured JSON with keys: 'ai_summary' and 'key_takeaways' (list of strings)."),
    ("user", "User Profile: {user_name}\nHabit Statistics:\n{stats_summary}\n\nGenerate productivity insights and performance evaluation.")
])
