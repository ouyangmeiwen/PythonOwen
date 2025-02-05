import os
from fastapi import APIRouter, Request
from app.utils.jwtutils import *
from app.dtos.token_dto import TokenDto
from app.middleware.rate_limit_middleware import *
from app.dtos.base_dto import *
from app.baseinit.configinit import *
# 创建路由实例
router_token = APIRouter()
# http://127.0.0.1:8000/token?username=1&password=2
# GET 请求示例
@router_token.get("/token",tags=["token"])
@limiter.limit("1000/day")  # 每秒最多1次请求
def token(request: Request,username: str = None, password: str = None):
    """
    **GET** 请求，生成token
    """
    # 用户数据
    user_data = {
        "username": username,  # 用户标识符，可以是用户名或用户 ID
        "password": password   # 角色信息
    }
    tokenstr=create_jwt_token(user_data,timedelta(hours=EXPIRES_HOURS))
    return {"token": tokenstr}

# http://127.0.0.1:8000/posttoken
@router_token.post("/posttoken",tags=["token"])
@limiter.limit("1000/day")  # 每秒最多1次请求
def posttoken(tokendto:TokenDto ,request: Request):
    """
    **POST** 请求，生成token
    """
    body=tokendto.model_dump()
    tokenstr=create_jwt_token(body,timedelta(hours=24))
    return {"token": tokenstr}


# http://127.0.0.1:8000/validtoken?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6IjEiLCJwYXNzd29yZCI6IjIiLCJleHAiOjE3Mzc2MjIwMjd9.4VuHCgH4ndSBFtU_iaeTKy8m4rhtMJHxm7mWvr0czbs
# GET 请求示例
@router_token.get("/validtoken",tags=["token"])
def token(request: Request,token: str = None):
    """
    **GET** 请求，校验token
    """
    result=verify_jwt_token(token)
    result["password"]="******"  #防止密码泄露
    return {"result": result}