#pip install slowapi
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from fastapi.responses import JSONResponse



# "5/minute"：每分钟最多 5 次请求。
# "100/hour"：每小时最多 100 次请求。
# "1000/day"：每天最多 1000 次请求。
# "10/second"：每秒最多 10 次请求。



# 初始化限流器
limiter = Limiter(key_func=get_remote_address)

# 自定义限流中间件
class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            # 直接调用 limiter 的速率限制装饰器
            response = await call_next(request)
            return response
        except RateLimitExceeded as e:
            # 超过限制时返回 429 错误
            return JSONResponse(
                status_code=429,
                content={"detail": "Rate limit exceeded, try again later."},
            )
