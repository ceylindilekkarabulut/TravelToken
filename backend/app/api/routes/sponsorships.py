import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.models.schemas import SponsorshipCreateRequest, SponsorshipResponse
from app.models.db import Sponsorship

router = APIRouter()


@router.post("/create", response_model=SponsorshipResponse)
async def create_sponsorship(body: SponsorshipCreateRequest, db: AsyncSession = Depends(get_db)):
    sponsorship = Sponsorship(
        id=str(uuid.uuid4()),
        goal_id=body.goal_id,
        sponsor_wallet=body.sponsor_wallet,
        amount_sol=body.amount_sol,
        tx_signature=body.tx_signature,
    )
    db.add(sponsorship)
    await db.commit()
    await db.refresh(sponsorship)
    return sponsorship
