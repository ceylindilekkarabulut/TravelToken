import asyncio
import json
from typing import Any, Callable
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.db import AgentLog
from app.utils.logger import get_logger

logger = get_logger(__name__)


async def record_agent_execution(
    goal_id: str,
    agent_name: str,
    input_state: dict[str, Any],
    agent_func: Callable,
    db: AsyncSession,
) -> dict:
    start_time = asyncio.get_event_loop().time()

    try:
        result = await agent_func(input_state)
        end_time = asyncio.get_event_loop().time()
        duration_ms = int((end_time - start_time) * 1000)

        log_entry = AgentLog(
            goal_id=goal_id,
            agent_name=agent_name,
            input_json=json.dumps(input_state, default=str),
            output_json=json.dumps(result, default=str),
            duration_ms=duration_ms,
        )
        db.add(log_entry)
        await db.flush()

        logger.info(
            "agent_execution_recorded",
            agent=agent_name,
            goal_id=goal_id,
            duration_ms=duration_ms,
        )

        return result
    except Exception as e:
        end_time = asyncio.get_event_loop().time()
        duration_ms = int((end_time - start_time) * 1000)

        error_result = {"error": str(e)}
        log_entry = AgentLog(
            goal_id=goal_id,
            agent_name=agent_name,
            input_json=json.dumps(input_state, default=str),
            output_json=json.dumps(error_result, default=str),
            duration_ms=duration_ms,
        )
        db.add(log_entry)
        await db.flush()

        logger.error(
            "agent_execution_failed",
            agent=agent_name,
            goal_id=goal_id,
            error=str(e),
            duration_ms=duration_ms,
        )

        raise
