from fastapi import Header, HTTPException
from logging import getLogger

logger = getLogger("Dependencies")


async def get_tsmc_uid(x_tsmc_uid: str = Header()):
    logger.info(f"Get X-TSMC-UID: {x_tsmc_uid}")
