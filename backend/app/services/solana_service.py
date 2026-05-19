import json
from pathlib import Path
from typing import Callable

from anchorpy import Program, Provider, Wallet, Idl
from solana.keypair import Keypair
from solana.publickey import PublicKey
from solana.rpc.async_api import AsyncClient

from app.config import settings
from app.utils.logger import get_logger

logger = get_logger(__name__)


def _load_keypair(path: str) -> Keypair:
    data = json.loads(Path(path).read_text())
    if isinstance(data, dict) and "secret_key" in data:
        secret_data = data["secret_key"]
    elif isinstance(data, dict) and "secretKey" in data:
        secret_data = data["secretKey"]
    elif isinstance(data, list):
        secret_data = data
    else:
        raise ValueError("Unsupported keypair format")
    return Keypair.from_secret_key(bytes(secret_data))


async def _load_program() -> tuple[Program, AsyncClient, Keypair]:
    authority_keypair = _load_keypair(settings.backend_authority_keypair_path)
    client = AsyncClient(settings.solana_rpc_url)
    wallet = Wallet(authority_keypair)
    idl_path = Path(__file__).resolve().parents[3] / "contracts" / "idl" / "travel_tokens.json"
    idl_data = json.loads(idl_path.read_text())
    idl = Idl.from_json(idl_data)
    program_id = PublicKey(idl.metadata.address)
    program = Program(idl, program_id, Provider(client, wallet))
    return program, client, authority_keypair


async def initialize_goal_on_chain(goal_id: str, user_wallet: str, budget_lamports: int) -> str:
    program, client, authority_keypair = await _load_program()
    try:
        goal_pda, _ = PublicKey.find_program_address(
            [b"goal", goal_id.encode("utf-8")], program.program_id
        )
        tx_sig = await program.rpc["initialize_goal"](
            goal_id,
            budget_lamports,
            ctx={
                "accounts": {
                    "travel_goal": str(goal_pda),
                    "traveler": str(authority_keypair.public_key),
                    "authority": str(authority_keypair.public_key),
                    "system_program": str(PublicKey("11111111111111111111111111111111")),
                },
                "signers": [authority_keypair],
            },
        )
        return tx_sig
    finally:
        await client.close()


async def release_funds(goal_id: str, recipient_wallet: str) -> str:
    program, client, authority_keypair = await _load_program()
    try:
        goal_pda, _ = PublicKey.find_program_address(
            [b"goal", goal_id.encode("utf-8")], program.program_id
        )
        tx_sig = await program.rpc["release_funds"](
            ctx={
                "accounts": {
                    "travel_goal": str(goal_pda),
                    "traveler": recipient_wallet,
                    "authority": str(authority_keypair.public_key),
                },
                "signers": [authority_keypair],
            },
        )
        return tx_sig
    finally:
        await client.close()


async def refund_sponsors(goal_id: str, sponsor_wallet: str) -> str:
    program, client, authority_keypair = await _load_program()
    try:
        goal_pda, _ = PublicKey.find_program_address(
            [b"goal", goal_id.encode("utf-8")], program.program_id
        )
        sponsor_pub = PublicKey(sponsor_wallet)
        sponsor_pda, _ = PublicKey.find_program_address(
            [b"sponsorship", bytes(goal_pda), bytes(sponsor_pub)], program.program_id
        )
        tx_sig = await program.rpc["refund_sponsor"](
            ctx={
                "accounts": {
                    "travel_goal": str(goal_pda),
                    "sponsorship": str(sponsor_pda),
                    "sponsor": str(sponsor_pub),
                    "authority": str(authority_keypair.public_key),
                },
                "signers": [authority_keypair],
            },
        )
        return tx_sig
    finally:
        await client.close()


async def listen_program_events(handler: Callable[[dict], None]) -> None:
    logger.info("Starting Solana event listener")
    # TODO: implement full subscription with real-time RPC logs and event parsing.
    return
