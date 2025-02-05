from fastapi import FastAPI
from app.api.item_api import router_items
from app.api.token_api import router_token
from app.api.libitem_api import router_libitem
import uvicorn
from app.middleware.rate_limit_middleware import *
from colorama import init, Fore
from app.middleware.logging_middleware import LoggingMiddleware
from app.utils.loggerutils import logger
from app.baseinit.configinit import *
from app.api.file_api import router_file

# 创建 FastAPI 实例
app = FastAPI(
    docs_url= "/docs",
    redoc_url= "/redoc",
    openapi_url="/openapi.json",
    title="Open API",
    description="This is a Open API for demonstration purposes.",
    version="1.0.0",
    contact={
        "name": "API Support",
        "url": "https://example.com/support",
        "email": "support@example.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
)

#禁用swagger
# app = FastAPI(
#     docs_url=None,    # 禁用 Swagger UI
#     redoc_url=None,   # 禁用 ReDoc
# )


#中间件注册
app.add_middleware(RateLimitMiddleware) # 将限流中间件添加到 FastAPI 应用
app.add_middleware(LoggingMiddleware) #日志中间件




# 包含模块化的路由
app.include_router(router_items)  #item
app.include_router(router_token)  #token
app.include_router(router_libitem)  #libitem
app.include_router(router_file) #file


# 启动 FastAPI 应用时指定端口
if __name__ == "__main__":
    # Get host and port from environment variables

    init()  #颜色字体初始化
    print(f"=================Swagger UI: {Fore.GREEN}http://127.0.0.1:{PORT}{app.docs_url}  {Fore.WHITE}==============")
    print(f"=====================ReDoc:: {Fore.GREEN}http://127.0.0.1:{PORT}{app.redoc_url} {Fore.WHITE}==============")
    logger.info(f"http://127.0.0.1:{PORT}{app.docs_url}")
    uvicorn.run(app, host=HOST,port=PORT)
