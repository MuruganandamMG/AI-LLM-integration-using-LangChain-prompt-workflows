import pytest
from app.ai.quote_chain import run_motivational_quote_chain

@pytest.mark.asyncio
async def test_quote_chain_mock():
    res = await run_motivational_quote_chain(user_name="John", category="Fitness")
    assert "quote" in res
    assert "author" in res
    assert "reflection_prompt" in res
