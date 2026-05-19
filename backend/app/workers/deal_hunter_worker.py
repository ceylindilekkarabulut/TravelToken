import asyncio
from celery import Celery
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from app.config import settings
from app.models.db import PriceHistory, TravelGoal
from app.services.amadeus_client import search_flights, search_hotels
from app.utils.logger import get_logger

logger = get_logger(__name__)
celery_app = Celery("throne_travel", broker=settings.redis_url, backend=settings.redis_url)
celery_app.conf.beat_schedule = {
    "scan-deals-every-30s": {
        "task": "app.workers.deal_hunter_worker.scan_all_active_goals",
        "schedule": 30.0,
    }
}
celery_app.conf.timezone = "UTC"


def _get_prices(origin: str, destination: str, travel_date: str) -> tuple[float, float]:
    flights = asyncio.run(search_flights(origin, destination, travel_date))
    hotels = asyncio.run(search_hotels(destination, travel_date))
    flight_price = float(flights[0].get("price", 0)) if flights else 0.0
    hotel_price = float(hotels[0].get("price", 0)) if hotels else 0.0
    return flight_price, hotel_price


@celery_app.task
def scan_all_active_goals():
    engine = create_engine(settings.database_url, future=True)
    with Session(engine) as session:
        results = session.execute(
            select(TravelGoal).where(TravelGoal.status == "complete")
        )
        goals = results.scalars().all()

        for goal in goals:
            try:
                flight_price, hotel_price = _get_prices(goal.origin, goal.destination, goal.travel_date)
                last_entry = session.execute(
                    select(PriceHistory)
                    .where(PriceHistory.goal_id == goal.id)
                    .order_by(PriceHistory.recorded_at.desc())
                    .limit(1)
                ).scalar_one_or_none()

                previous_total = (last_entry.flight_price_usd or 0.0) + (last_entry.hotel_price_usd or 0.0) if last_entry else float("inf")
                current_total = flight_price + hotel_price
                is_buy_signal = previous_total != float("inf") and current_total < previous_total * 0.95

                record = PriceHistory(
                    goal_id=goal.id,
                    flight_price_usd=flight_price,
                    hotel_price_usd=hotel_price,
                    is_buy_signal=is_buy_signal,
                )
                session.add(record)
                session.commit()
                logger.info("price_history_recorded", goal_id=goal.id, current_total=current_total, is_buy_signal=is_buy_signal)
            except Exception as exc:
                session.rollback()
                logger.error("deal_hunter_scan_error", error=str(exc), goal_id=goal.id)
