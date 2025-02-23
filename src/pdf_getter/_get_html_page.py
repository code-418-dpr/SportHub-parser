import httpx

from src.logger import get_logger

logger = get_logger(__name__)


async def get_html_page(client: httpx.AsyncClient, url: str) -> str | None:
    try:
        response = await client.get(url)
    except:  # noqa: E722
        logger.exception("Error when retrieving an HTML page of the site")
        return None
    else:
        logger.info("HTML page retrieved")
        return response.text
