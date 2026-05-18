from celery import Celery
from app.config import settings

celery_app = Celery("throne_travel", broker=settings.redis_url, backend=settings.redis_url)
celery_app.conf.beat_schedule = {
    "scan-deals-every-30s": {
        "task": "app.workers.deal_hunter_worker.scan_all_active_goals",
        "schedule": 30.0,
    }
}


@celery_app.task
def scan_all_active_goals():
    # TODO: query active goals, run deal hunter, push WS notification if price drops
    pass
