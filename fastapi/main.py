import uvicorn
from app.middleware.rate_limit_middleware import *
from colorama import init, Fore
from app.utils.loggerutils import logger
from app.baseinit.configinit import *
from app.baseinit.app_init import appinit
from app.baseinit.middleware_init import middlewareinit
from app.baseinit.router_init import routerinit
#初始化app
app=appinit()
#中间件注册
middlewareinit(app)
# 包含模块化的路由
routerinit(app)

# 启动 FastAPI 应用时指定端口
if __name__ == "__main__":
    # Get host and port from environment variables
    init()  #颜色字体初始化
    print(f"=================Swagger UI: {Fore.GREEN}http://127.0.0.1:{PORT}{app.docs_url}  {Fore.WHITE}==============")
    print(f"=====================ReDoc:: {Fore.GREEN}http://127.0.0.1:{PORT}{app.redoc_url} {Fore.WHITE}==============")
    logger.info(f"http://127.0.0.1:{PORT}{app.docs_url}")
    logger.info(f"http://127.0.0.1:9002/docs")
    uvicorn.run(app, host=HOST,port=PORT)
