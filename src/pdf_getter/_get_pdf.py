from pathlib import Path

import aiofiles
import httpx
from dotenv import load_dotenv

from src.conf import PDF_FILE_URL, TMP_PATH
from src.logger import get_logger
from src.pdf_getter._download_file import download_file
from src.pdf_getter._get_html_page import get_html_page
from src.pdf_getter._parse_file_url import parse_file_url

load_dotenv()
PREV_URL_PATH = TMP_PATH / "prev_url.txt"
PDF_FILE_PATH = TMP_PATH / "table.pdf"

logger = get_logger(__name__)


async def get_pdf_file(local_only: bool = False) -> Path | None:
    logger.info(
        "Getting the PDF file and the info about it",
        extra={"is_local_only": local_only},
    )
    result = None

    async with httpx.AsyncClient(verify=False) as client:  # noqa: S501
        if local_only:
            if PDF_FILE_PATH.exists():
                result = PDF_FILE_PATH
            else:
                logger.error("File not found")
            return result

        page = await get_html_page(client, PDF_FILE_URL)
        if not page:
            return result

        file_url = parse_file_url(page)
        if not file_url:
            return result

        changed = False
        if PREV_URL_PATH.exists():
            async with aiofiles.open(PREV_URL_PATH) as file:
                prev_url = await file.read()
        else:
            TMP_PATH.mkdir(exist_ok=True)
            prev_url = None
        if prev_url != file_url:
            async with aiofiles.open(PREV_URL_PATH, "w") as file:
                await file.write(file_url)
            changed = True

        if not changed:
            logger.info("File not changed")
            result = PDF_FILE_PATH
        else:
            logger.info("File changed")
            is_file_downloaded = await download_file(client, PDF_FILE_PATH, file_url)
            if is_file_downloaded:
                logger.info("File downloaded")
                result = PDF_FILE_PATH
        return result
