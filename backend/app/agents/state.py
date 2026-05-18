from typing import TypedDict, Annotated
from operator import add


class TravelState(TypedDict):
    goal_id: str
    origin: str
    destination: str
    travel_date: str
    budget_usd: float
    preferences: str

    route_result: dict | None
    deal_result: dict | None
    budget_result: dict | None
    final_report_md: str | None

    errors: Annotated[list[str], add]
    sse_events: Annotated[list[dict], add]
