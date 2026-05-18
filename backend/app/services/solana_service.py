from app.utils.logger import get_logger

logger = get_logger(__name__)


async def initialize_goal_on_chain(goal_id: str, user_wallet: str, budget_lamports: int) -> str:
    # TODO: implement with anchorpy + solana-py
    logger.info("initialize_goal_on_chain", goal_id=goal_id, wallet=user_wallet)
    return "mock_pda_address"


async def release_funds(goal_pda: str, recipient_wallet: str) -> str:
    # TODO: implement with anchorpy
    logger.info("release_funds", pda=goal_pda, recipient=recipient_wallet)
    return "mock_tx_signature"


async def refund_sponsors(goal_pda: str) -> str:
    # TODO: implement with anchorpy
    logger.info("refund_sponsors", pda=goal_pda)
    return "mock_tx_signature"
