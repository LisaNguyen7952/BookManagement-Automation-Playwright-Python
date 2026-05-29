
import logging
import os
from datetime import datetime

from configs.other_config import LOG_DIR


# ===== Logger setup =====
def get_logger(name=__name__):
    log = logging.getLogger(name)
    log.setLevel(logging.INFO)

    if not log.handlers:
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

        # Console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch.setFormatter(formatter)
        log.addHandler(ch)

        # File handler
        os.makedirs(LOG_DIR, exist_ok=True)
        log_file = os.path.join(LOG_DIR, f"test_log_{datetime.now().strftime('%Y-%m-%d')}.log")
        fh = logging.FileHandler(log_file, mode="a", encoding="utf-8")
        fh.setLevel(logging.INFO)
        fh.setFormatter(formatter)
        log.addHandler(fh)

    return log

logger = get_logger()
