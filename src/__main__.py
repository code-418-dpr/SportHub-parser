from fastapi import FastAPI, Response, status

from src.conf import LOCAL_PDF_ONLY, TMP_PATH
from src.logger import get_logger
from src.process import process

OUTPUT_PATH = TMP_PATH / "table.pdf"

logger = get_logger(__name__)
app = FastAPI()


@app.post("/run-parser")
async def run_parser(response: Response) -> Response:
    try:
        result = await process(LOCAL_PDF_ONLY)
    except:  # noqa: E722
        logger.exception("Unexpected error")
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    else:
        response.status_code = status.HTTP_200_OK if result else status.HTTP_400_BAD_REQUEST
    return response


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)  # noqa: S104
