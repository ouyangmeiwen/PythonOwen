import os
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
import time
import logging.config
from app.utils.stringutils import StringUtils
from app.baseinit.configinit import *

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
        "file": {
            "class": "logging.FileHandler",
            "filename": "fastapi.log",  # 日志文件
            "formatter": "default",
        },
    },
    "root": {
        "handlers": ["console", "file"],
        "level": f"{LOG_LEVEL}",
    },
}

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger("fast_api")