import logging
import os

LOG_FILE = os.getenv("AUTH_LOG_FILE", "auth.log")

logger = logging.getLogger("auth_logger")
logger.setLevel(logging.INFO)

# evitar múltiplos handlers em execuções repetidas
if not logger.handlers:
    handler = logging.FileHandler(LOG_FILE)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
