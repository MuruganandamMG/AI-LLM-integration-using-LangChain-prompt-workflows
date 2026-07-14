from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from app.ai.factory import LLMFactory

QUOTE_PROMPT = ChatPromptTemplate.from_messages([
    ("system", "You are an inspiring personal growth mentor. Generate a powerful, context-aware motivational quote and reflection prompt for the user in JSON format with keys: 'quote', 'author', 'reflection_prompt'."),
    ("user", "User Name: {user_name}\nCurrent Category: {category}\n\nGenerate motivational reflection.")
])

async def run_motivational_quote_chain(user_name: str, category: str = "General") -> dict:
    llm = LLMFactory.get_llm()
    if llm is None:
        return {
            "quote": "We are what we repeatedly do. Excellence, then, is not an act, but a habit.",
            "author": "Will Durant",
            "reflection_prompt": f"How will you bring excellence to your {category} goals today, {user_name}?",
            "provider": "mock"
        }
    chain = QUOTE_PROMPT | llm | JsonOutputParser()
    try:
        return await chain.ainvoke({"user_name": user_name, "category": category})
    except Exception:
        return {
            "quote": "Small disciplines repeated with consistency every day lead to great achievements.",
            "author": "John C. Maxwell",
            "reflection_prompt": "What small step can you take right now?",
            "provider": "fallback"
        }
