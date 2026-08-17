import pytest
from app.ai.factory import LLMFactory
from app.ai.growth_chain import run_growth_recommendation_chain
from app.ai.analytics_chain import run_productivity_analytics_chain

@pytest.mark.asyncio
async def test_growth_chain_mock():
    habits = [{"title": "Exercise", "category": "Fitness", "logs_count": 5}]
    result = await run_growth_recommendation_chain(user_name="Alice", habits=habits)
    assert "title" in result
    assert "action_items" in result
    assert isinstance(result["action_items"], list)

@pytest.mark.asyncio
async def test_analytics_chain_mock():
    stats = {"total_habits": 3, "completion_rate": 85.0, "streak": 7}
    result = await run_productivity_analytics_chain(user_name="Alice", stats=stats)
    assert "ai_summary" in result
    assert "key_takeaways" in result
