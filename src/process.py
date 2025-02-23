import asyncio

import httpx

from src.conf import BACKEND_DATA_ROUTE_URL, TMP_PATH
from src.logger import get_logger
from src.pdf_getter import get_pdf_file
from src.pdf_parser import parse_pdf_file

PREV_URL_PATH = TMP_PATH / "prev_url.txt"
PDF_FILE_PATH = TMP_PATH / "table.pdf"

logger = get_logger(__name__)


async def process(local_pdf_only: bool = False) -> bool:
    pdf_file_path = await get_pdf_file(local_pdf_only)
    if not pdf_file_path:
        return False

    async with httpx.AsyncClient() as client:
        for num, chunk in enumerate(parse_pdf_file(pdf_file_path), 1):
            response = await client.post(
                BACKEND_DATA_ROUTE_URL,
                json=chunk,
                timeout=60,
            )
            if num % 100 == 0:
                logger.info("Processed %s pages", num)
                await asyncio.sleep(10)
            if response.status_code not in (200, 201):
                logger.error(
                    "%s while sending data to server",
                    response.status_code,
                    extra={"json": response.json()},
                )
                return False
    return True
