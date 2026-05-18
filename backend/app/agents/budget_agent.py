from app.agents.state import TravelState
from app.services.llm_client import chat_completion
from app.utils.logger import get_logger

logger = get_logger(__name__)

FOOD_COST_PER_DAY = {
    "TR": 20, "DE": 50, "FR": 60, "US": 55, "JP": 45, "TH": 15,
}


async def run_budget_agent(state: TravelState) -> dict:
    try:
        deal = state.get("deal_result") or {}
        flight = deal.get("best_flight") or {}
        hotel = deal.get("best_hotel") or {}

        flight_price = flight.get("price", 0) if isinstance(flight, dict) else 0
        hotel_price = hotel.get("price", 0) if isinstance(hotel, dict) else 0

        country_code = state["destination"][:2].upper()
        food_per_day = FOOD_COST_PER_DAY.get(country_code, 40)
        days = 7
        food_total = food_per_day * days

        total_usd = flight_price + hotel_price + food_total

        prompt = (
            f"Trip from {state['origin']} to {state['destination']}. "
            f"Estimated cost: flight ${flight_price}, hotel ${hotel_price}, food ${food_total}. "
            f"Budget: ${state['budget_usd']}. Give 3 actionable money-saving tips."
        )
        tips = await chat_completion(prompt)

        return {
            "flight_usd": flight_price,
            "hotel_usd": hotel_price,
            "food_usd": food_total,
            "total_usd": total_usd,
            "within_budget": total_usd <= state["budget_usd"],
            "tips": tips,
        }
    except Exception as e:
        logger.error("budget_agent_error", error=str(e))
        return {"total_usd": 0, "tips": str(e)}
