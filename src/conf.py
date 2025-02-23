import logging
import os

from dotenv import load_dotenv

is_dotenv_loaded = load_dotenv()

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

SEQ_API_KEY = os.getenv("SEQ_API_KEY")
SEQ_URL = os.getenv("SEQ_URL")
