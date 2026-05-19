import asyncio
import googlemaps
from app.config import settings
from app.utils.logger import get_logger

logger = get_logger(__name__)


async def get_route_directions(origin: str, destination: str) -> dict:
    if not settings.google_maps_api_key:
        return {
            "distance": "4h 20m",
            "duration": "4h 20m",
            "steps": [
                f"Start from {origin}",
                f"Head towards {destination}",
                "Follow main highways",
                "Arrive at destination",
            ],
        }

    loop = asyncio.get_running_loop()

    def fetch_directions():
        gmaps = googlemaps.Client(key=settings.google_maps_api_key)
        return gmaps.directions(origin, destination, mode="transit")

    try:
        result = await loop.run_in_executor(None, fetch_directions)
        if result:
            leg = result[0]["legs"][0]
            return {
                "distance": leg["distance"]["text"],
                "duration": leg["duration"]["text"],
                "steps": [s["html_instructions"] for s in leg["steps"][:5]],
            }
        return {"distance": "N/A", "duration": "N/A", "steps": []}
    except Exception as e:
        logger.error("maps_error", error=str(e))
        return {"distance": "N/A", "duration": "N/A", "steps": []}
