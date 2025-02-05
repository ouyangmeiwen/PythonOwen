from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
import time
from app.utils.stringutils import StringUtils
from app.utils.loggerutils import logger

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        uuid=StringUtils.generate_uuid32()
        logger.info(f"{uuid} Request: {request.method} {request.url}")
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        logger.info(f"{uuid} Response: {response.status_code}, Time: {process_time:.3f}s")
        return response


