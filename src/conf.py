import logging
import os

from dotenv import load_dotenv

load_dotenv()

LOCAL_PDF_ONLY = bool(os.getenv("LOCAL_PDF_ONLY"))
PDF_FILE_URL = os.getenv("PDF_FILE_URL")
BACKEND_DATA_ROUTE_URL = os.getenv("BACKEND_DATA_ROUTE_URL")
if not PDF_FILE_URL or not BACKEND_DATA_ROUTE_URL:
    error_msg = "PDF_FILE_URL или BACKEND_DATA_ROUTE_URL не заданы"
    raise ValueError(error_msg)

LOG_LEVEL = os.getenv("LOG_LEVEL", logging.WARNING)
if LOG_LEVEL not in ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"):
    error_msg = "LOG_LEVEL должен иметь одно из этих значений: DEBUG, INFO, WARNING, ERROR, CRITICAL"
    raise ValueError(error_msg)

logging.basicConfig(
    encoding="utf-8",
    level=LOG_LEVEL,
    filemode="w",
    format="%(name)s [%(asctime)s] %(levelname)s %(message)s",
)
logging.getLogger("httpcore").setLevel(logging.WARNING)
