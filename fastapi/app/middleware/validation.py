
from fastapi import HTTPException, Security,Depends
from fastapi.security import OAuth2PasswordBearer
import os
from fastapi import Header
from app.utils.jwtutils import *
from app.baseinit.configinit import *
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# 模拟一个简单的 token 验证
def verify_token(token: str = Depends(oauth2_scheme)):
    check_token= verify_jwt_token(token)
    if check_token:
        return check_token
    raise HTTPException(status_code=401, detail="Invalid or missing token")

# 依赖项：从请求头获取 token
def get_token(authorization: str = Header(None)):
    if authorization is None:
        return None
    # 假设 token 使用 Bearer 方式传递
    if "Bearer" in authorization:
        return authorization.split(" ")[1]
    raise HTTPException(status_code=400, detail="Invalid authorization header")

def verify_authorization(token: str = Depends(get_token)):
    if ENABLE_AUTH and token is None:
        raise HTTPException(status_code=401, detail="Token is required")
    if ENABLE_AUTH:
        verify_token(token)