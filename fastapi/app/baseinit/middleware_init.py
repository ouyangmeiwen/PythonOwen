from fastapi import FastAPI
from app.middleware.rate_limit_middleware import *
from app.middleware.logging_middleware import LoggingMiddleware


def middlewareinit(app:FastAPI):
    app.add_middleware(RateLimitMiddleware) # 将限流中间件添加到 FastAPI 应用
    app.add_middleware(LoggingMiddleware) #日志中间件