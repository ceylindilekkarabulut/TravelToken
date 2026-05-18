import json
from pathlib import Path
from solders.keypair import Keypair
from solders.rpc.responses import GetAccountInfoResp
from solana.rpc.async_api import AsyncClient

from app.config import settings
from app.utils.logger import get_logger

logger = get_logger(__name__)

PROGRAM_ID = "Fg6PaFpoGXkYsidMpWTK6W2BeZ7FEfcYkg476zPFsLnS"

_client: AsyncClient | None = None
_authority_keypair: Keypair | None = None


async def get_rpc_client() -> AsyncClient:
    global _client
    if _client is None:
        _client = AsyncClient(settings.solana_rpc_url)
    return _client


async def get_authority_keypair() -> Keypair:
    global _authority_keypair
    if _authority_keypair is None:
        keypair_path = Path(settings.backend_authority_keypair_path)
        if not keypair_path.exists():
            logger.error("authority_keypair_not_found", path=str(keypair_path))
            raise FileNotFoundError(f"Authority keypair not found at {keypair_path}")
        with open(keypair_path, "r") as f:
            keypair_bytes = json.load(f)
        _authority_keypair = Keypair.from_secret_key(bytes(keypair_bytes[:32]))
    return _authority_keypair


async def initialize_goal_on_chain(goal_id: str, user_wallet: str, budget_lamports: int) -> str:
    try:
        client = await get_rpc_client()
        authority = await get_authority_keypair()

        logger.info(
            "initialize_goal_on_chain_start",
            goal_id=goal_id,
            wallet=user_wallet,
            budget_lamports=budget_lamports,
        )

        seed = b"goal" + goal_id.encode()[:28]
        pda, bump = await _get_pda(seed)

        logger.info("initialize_goal_on_chain_success", pda=str(pda), goal_id=goal_id)
        return str(pda)
    except Exception as e:
        logger.error("initialize_goal_on_chain_error", error=str(e), goal_id=goal_id)
        raise


async def release_funds(goal_pda: str, recipient_wallet: str) -> str:
    try:
        client = await get_rpc_client()
        authority = await get_authority_keypair()

        logger.info(
            "release_funds_start",
            pda=goal_pda,
            recipient=recipient_wallet,
        )

        tx_signature = f"mock_release_{goal_pda[:8]}"

        logger.info("release_funds_success", tx_signature=tx_signature)
        return tx_signature
    except Exception as e:
        logger.error("release_funds_error", error=str(e), pda=goal_pda)
        raise


async def refund_sponsors(goal_pda: str) -> str:
    try:
        client = await get_rpc_client()
        authority = await get_authority_keypair()

        logger.info("refund_sponsors_start", pda=goal_pda)

        tx_signature = f"mock_refund_{goal_pda[:8]}"

        logger.info("refund_sponsors_success", tx_signature=tx_signature)
        return tx_signature
    except Exception as e:
        logger.error("refund_sponsors_error", error=str(e), pda=goal_pda)
        raise


async def _get_pda(seed: bytes) -> tuple:
    from solders.pubkey import Pubkey

    program_id = Pubkey.from_string(PROGRAM_ID)
    try:
        pda, bump = Pubkey.find_program_address([seed], program_id)
        return pda, bump
    except Exception as e:
        logger.error("pda_derivation_error", error=str(e))
        raise

