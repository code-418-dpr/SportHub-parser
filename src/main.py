import logging
from pathlib import Path

from fastapi import FastAPI, Response, status

from .conf import LOCAL_PDF_ONLY
from .process import process

OUTPUT_PATH = Path("tmp/table.pdf")

logger = logging.getLogger(__name__)
app = FastAPI()


@app.post("/run-parser")
async def run_parser(response: Response) -> Response:
    try:
        result = await process(LOCAL_PDF_ONLY)
    except:  # noqa: E722
        logger.critical("Непредусмотренная ошибка")
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    else:
        response.status_code = status.HTTP_200_OK if result else status.HTTP_400_BAD_REQUEST
    return response


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=3000)  # noqa: S104
