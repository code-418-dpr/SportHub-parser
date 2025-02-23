import re
import typing
from pathlib import Path

import pymupdf

from src.logger import get_logger
from src.pdf_parser import _pdf_page_text

FIRST_PAGE_REGEX = re.compile(r"^(.+\n)*\(чел\.\)")

logger = get_logger(__name__)


def parse(
    pdf_path: Path,
    page_nums: tuple[int] | None = None,
) -> typing.Generator[list[dict]]:
    logger.info(
        "Extracting text from %s pages of the %s",
        page_nums if page_nums else "all",
        pdf_path,
    )
    doc = pymupdf.open(pdf_path)

    logger.info("Parsing the raw text of the pages")
    for page_num in page_nums if page_nums else range(doc.page_count):
        page = doc[page_num].get_text()
        if page_num == 0:
            page = FIRST_PAGE_REGEX.sub("", page, count=1)
        yield _pdf_page_text.parse(page)

    logger.info("File successfully parsed")
