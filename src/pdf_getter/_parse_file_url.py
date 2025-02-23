import re

from src.logger import get_logger

BASE_URL = "https://storage.minsport.gov.ru/cms-uploads/cms/"
NEEDED_URL_PATTERN = re.compile(r"(II_chast_EKP_.+?\.pdf)")

logger = get_logger(__name__)


def parse_file_url(html: str) -> str | None:
    match = NEEDED_URL_PATTERN.search(html)
    if match:
        return BASE_URL + match.group(1)

    logger.error("The file URL not found in the HTML. Maybe you should update the regexp")
    return None
