from app.agents.state import TravelState
from app.services.amadeus_client import search_flights, search_hotels
from app.services.llm_client import chat_completion
from app.utils.logger import get_logger

logger = get_logger(__name__)


async def run_deal_hunter_agent(state: TravelState) -> dict:
    try:
        flights = await search_flights(
            state["origin"], state["destination"], state["travel_date"]
        )
        hotels = await search_hotels(state["destination"], state["travel_date"])

        best_flight = min(flights, key=lambda f: f.get("price", 9999), default={})
        best_hotel = min(hotels, key=lambda h: h.get("price", 9999), default={})

        prompt = (
            f"Interpret these travel deals for {state['destination']}:\n"
            f"Best flight: {best_flight}\nBest hotel: {best_hotel}\n"
            f"Budget: ${state['budget_usd']}. Give a short deal quality assessment."
        )
        assessment = await chat_completion(prompt)

        return {
            "best_flight": best_flight,
            "best_hotel": best_hotel,
            "assessment": assessment,
            "all_flights": flights[:5],
            "all_hotels": hotels[:5],
        }
    except Exception as e:
        logger.error("deal_hunter_error", error=str(e))
        return {"best_flight": "N/A", "best_hotel": "N/A", "assessment": str(e)}
