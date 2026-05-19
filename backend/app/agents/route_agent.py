from app.agents.state import TravelState
from app.services.maps_client import get_route_directions
from app.services.llm_client import chat_completion
from app.utils.logger import get_logger

logger = get_logger(__name__)


async def run_route_agent(state: TravelState) -> dict:
    try:
        directions = await get_route_directions(state["origin"], state["destination"])
        prompt = (
            f"Analyze this travel route from {state['origin']} to {state['destination']} "
            f"on {state['travel_date']}. Directions data: {directions}. "
            f"User preferences: {state['preferences']}. "
            "Provide a concise travel summary with key highlights and tips."
        )
        summary = await chat_completion(prompt)
        return {"summary": summary, "directions": directions}
    except Exception as e:
        logger.error("route_agent_error", error=str(e))
        return {"summary": f"Route analysis unavailable: {e}", "directions": {}}
