import logging
import re

BASE_URL = "https://storage.minsport.gov.ru/cms-uploads/cms/"
NEEDED_URL_PATTERN = re.compile(r"(II_chast_EKP_.+?\.pdf)")

logger = logging.getLogger(__name__)


def parse_file_url(html: str) -> str | None:
    match = NEEDED_URL_PATTERN.search(html)
    if match:
        return BASE_URL + match.group(1)

    logger.error(
        "Не найден URL файла в HTML. Вероятно, нужно сменить регулярное выражение",  # noqa: RUF001
    )
    return None
