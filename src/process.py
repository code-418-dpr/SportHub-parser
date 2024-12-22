import asyncio
import logging
from pathlib import Path

import httpx

from .conf import BACKEND_DATA_ROUTE_URL
from .pdf_getter import get_pdf_file
from .pdf_parser import parse_pdf_file

PREV_URL_PATH = Path("tmp/prev_url.txt")
PDF_FILE_PATH = Path("tmp/table.pdf")

logger = logging.getLogger(__name__)


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
                logger.info("Обработано %s страниц", num)
                await asyncio.sleep(10)
            if response.status_code not in (200, 201):
                logger.error(
                    "Ошибка %s при отправке данных на сервер: %s",
                    response.status_code,
                    response.json(),
                )
                return False
    return True
