import googlemaps
from app.config import settings
from app.utils.logger import get_logger

logger = get_logger(__name__)


async def get_route_directions(origin: str, destination: str) -> dict:
    try:
        gmaps = googlemaps.Client(key=settings.google_maps_api_key)
        result = gmaps.directions(origin, destination, mode="transit")
        if result:
            leg = result[0]["legs"][0]
            return {
                "distance": leg["distance"]["text"],
                "duration": leg["duration"]["text"],
                "steps": [s["html_instructions"] for s in leg["steps"][:5]],
            }
        return {}
    except Exception as e:
        logger.error("maps_error", error=str(e))
        return {"distance": "N/A", "duration": "N/A", "steps": []}
