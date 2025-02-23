from pathlib import Path

import aiofiles
import httpx

from src.logger import get_logger

logger = get_logger(__name__)


async def download_file(http_client: httpx.AsyncClient, path: Path, url: str) -> bool:
    logger.info("Downloading the file", extra={"url": url})

    try:
        async with (
            http_client.stream("GET", url) as response,
            aiofiles.open(path, "wb") as file,
        ):
            async for chunk in response.aiter_bytes():
                await file.write(chunk)
    except:  # noqa: E722
        logger.exception("Error when downloading the file")
        return False
    else:
        logger.info("File downloaded")
        return True
