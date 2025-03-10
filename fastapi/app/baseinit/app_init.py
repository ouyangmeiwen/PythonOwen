from fastapi import FastAPI


def appinit()->FastAPI:
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
    return app
