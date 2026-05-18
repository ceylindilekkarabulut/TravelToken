from datetime import datetime
from pydantic import BaseModel


class GoalCreateRequest(BaseModel):
    user_wallet: str
    destination: str
    origin: str
    travel_date: str
    budget_usd: float
    preferences: str = ""


class GoalResponse(BaseModel):
    id: str
    user_wallet: str
    destination: str
    origin: str
    travel_date: str
    budget_usd: float
    status: str
    final_report_md: str | None
    solana_goal_pda: str | None
    created_at: datetime

    class Config:
        from_attributes = True


class SponsorshipCreateRequest(BaseModel):
    goal_id: str
    sponsor_wallet: str
    amount_sol: float
    tx_signature: str | None = None


class SponsorshipResponse(BaseModel):
    id: str
    goal_id: str
    sponsor_wallet: str
    amount_sol: float
    tx_signature: str | None
    refunded: bool
    created_at: datetime

    class Config:
        from_attributes = True


class RouteSearchRequest(BaseModel):
    query: str
    origin: str | None = None
    destination: str | None = None
    limit: int = 10


class RouteResponse(BaseModel):
    id: str
    origin: str
    destination: str
    description_md: str
    tags: str
    copy_count: int
    creator_wallet: str | None
    created_at: datetime

    class Config:
        from_attributes = True
