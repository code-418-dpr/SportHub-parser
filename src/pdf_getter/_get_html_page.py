import logging

import httpx

logger = logging.getLogger(__name__)


async def get_html_page(client: httpx.AsyncClient, url: str) -> str | None:
    try:
        response = await client.get(url)
    except:
        logger.exception("Ошибка при получении HTML-страницы сайта")
        return None
    else:
        logger.info("HTML-страница получена")
        return response.text
