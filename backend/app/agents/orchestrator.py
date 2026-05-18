import asyncio
import json
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from app.agents.state import TravelState
from app.agents.route_agent import run_route_agent
from app.agents.deal_hunter_agent import run_deal_hunter_agent
from app.agents.budget_agent import run_budget_agent
from app.agents.logging_utils import record_agent_execution
from app.models.schemas import GoalCreateRequest
from app.utils.logger import get_logger

logger = get_logger(__name__)


def _sse(event: str, data: dict) -> str:
    return f"event: {event}\ndata: {json.dumps(data)}\n\n"


async def run_goal_pipeline(
    goal_id: str, body: GoalCreateRequest, db: AsyncSession
) -> AsyncGenerator[str, None]:
    state: TravelState = {
        "goal_id": goal_id,
        "origin": body.origin,
        "destination": body.destination,
        "travel_date": body.travel_date,
        "budget_usd": body.budget_usd,
        "preferences": body.preferences,
        "route_result": None,
        "deal_result": None,
        "budget_result": None,
        "final_report_md": None,
        "errors": [],
        "sse_events": [],
    }

    yield _sse("agent_start", {"agent": "route", "goal_id": goal_id})
    yield _sse("agent_start", {"agent": "deal_hunter", "goal_id": goal_id})

    route_task = asyncio.create_task(
        record_agent_execution(goal_id, "route", state, run_route_agent, db)
    )
    deal_task = asyncio.create_task(
        record_agent_execution(goal_id, "deal_hunter", state, run_deal_hunter_agent, db)
    )

    route_result, deal_result = await asyncio.gather(route_task, deal_task)
    state["route_result"] = route_result
    state["deal_result"] = deal_result

    yield _sse("agent_complete", {"agent": "route", "data": route_result})
    yield _sse("agent_complete", {"agent": "deal_hunter", "data": deal_result})

    yield _sse("agent_start", {"agent": "budget", "goal_id": goal_id})
    budget_result = await record_agent_execution(
        goal_id, "budget", state, run_budget_agent, db
    )
    state["budget_result"] = budget_result
    yield _sse("agent_complete", {"agent": "budget", "data": budget_result})

    await db.commit()

    final_report = _compile_report(state)
    state["final_report_md"] = final_report

    yield _sse("done", {"goal_id": goal_id, "report": final_report})


def _compile_report(state: TravelState) -> str:
    route = state.get("route_result") or {}
    deal = state.get("deal_result") or {}
    budget = state.get("budget_result") or {}

    return f"""# Travel Plan: {state['origin']} → {state['destination']}

## Route Overview
{route.get('summary', 'N/A')}

## Best Deals Found
- **Flight**: {deal.get('best_flight', 'N/A')}
- **Hotel**: {deal.get('best_hotel', 'N/A')}

## Budget Breakdown
- Total Estimated: ${budget.get('total_usd', 'N/A')}
- Savings Tips: {budget.get('tips', '')}
"""
