import httpx
from app.config import settings
from app.utils.logger import get_logger

logger = get_logger(__name__)

AMADEUS_BASE = "https://test.api.amadeus.com"
_token_cache: dict = {}


async def _get_token() -> str:
    if _token_cache.get("access_token"):
        return _token_cache["access_token"]

    async with httpx.AsyncClient() as client:
        r = await client.post(
            f"{AMADEUS_BASE}/v1/security/oauth2/token",
            data={
                "grant_type": "client_credentials",
                "client_id": settings.amadeus_client_id,
                "client_secret": settings.amadeus_client_secret,
            },
        )
        r.raise_for_status()
        data = r.json()
        _token_cache["access_token"] = data["access_token"]
        return data["access_token"]


async def search_flights(origin: str, destination: str, date: str) -> list[dict]:
    try:
        token = await _get_token()
        async with httpx.AsyncClient() as client:
            r = await client.get(
                f"{AMADEUS_BASE}/v2/shopping/flight-offers",
                headers={"Authorization": f"Bearer {token}"},
                params={
                    "originLocationCode": origin[:3].upper(),
                    "destinationLocationCode": destination[:3].upper(),
                    "departureDate": date,
                    "adults": 1,
                    "max": 5,
                },
            )
            r.raise_for_status()
            offers = r.json().get("data", [])
            return [
                {
                    "id": o["id"],
                    "price": float(o["price"]["total"]),
                    "carrier": o["validatingAirlineCodes"][0] if o.get("validatingAirlineCodes") else "",
                }
                for o in offers
            ]
    except Exception as e:
        logger.error("amadeus_flight_error", error=str(e))
        return []


async def search_hotels(destination: str, check_in: str) -> list[dict]:
    # Amadeus hotel search requires city code; simplified mock fallback
    return [
        {"id": "mock-hotel-1", "name": f"Hotel in {destination}", "price": 80.0},
        {"id": "mock-hotel-2", "name": f"Budget Inn {destination}", "price": 45.0},
    ]
