import pytest
from app.agents.budget_agent import run_budget_agent
from app.agents.state import TravelState


@pytest.fixture
def base_state() -> TravelState:
    return {
        "goal_id": "test-123",
        "origin": "Istanbul",
        "destination": "Paris",
        "travel_date": "2026-07-01",
        "budget_usd": 1500.0,
        "preferences": "budget travel",
        "route_result": None,
        "deal_result": {"best_flight": {"price": 300}, "best_hotel": {"price": 80}},
        "budget_result": None,
        "final_report_md": None,
        "errors": [],
        "sse_events": [],
    }


@pytest.mark.asyncio
async def test_budget_agent_within_budget(base_state, monkeypatch):
    async def mock_chat(_prompt):
        return "Use budget airlines and cook your own meals."

    monkeypatch.setattr("app.agents.budget_agent.chat_completion", mock_chat)
    result = await run_budget_agent(base_state)
    assert "total_usd" in result
    assert result["within_budget"] is True
