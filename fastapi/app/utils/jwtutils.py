import jwt
import os
from datetime import datetime, timedelta,timezone
from fastapi import HTTPException
from app.baseinit.configinit import *


# 生成 JWT token
def create_jwt_token(data: dict, expires_delta: timedelta = timedelta(hours=1)):
    """
    生成 JWT Token
    :param data: 要包含在 payload 中的用户数据
    :param expires_delta: token 的有效时长，默认为 1 小时
    :return: 生成的 JWT Token 字符串
    """
    to_encode = data.copy()
    expiration = datetime.now(timezone.utc) + expires_delta  # 使用 timezone.utc 获取当前 UTC 时间
    to_encode.update({"exp": expiration})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# 验证 JWT token
def verify_jwt_token(token: str):
    """
    验证 JWT Token
    :param token: 传入的 JWT Token 字符串
    :return: 解码后的 token 数据（payload）
    :raises HTTPException: 如果验证失败抛出异常
    """
    try:
        # 解码 JWT token
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded_token
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.DecodeError:
        raise HTTPException(status_code=400, detail="Failed to decode token")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=400, detail="Invalid token format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    
# 解析 JWT token（不验证）
def parse_jwt_token(token: str):
    """
    解析 JWT Token（不进行验证）
    :param token: 传入的 JWT Token 字符串
    :return: 解码后的 token 数据（payload），如果解析失败抛出异常
    """
    try:
        # 解码 JWT token 但不进行验证
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], verify=False)
        return decoded_token
    except jwt.JWTError:
        raise HTTPException(status_code=403, detail="Invalid token")
    

# 刷新 Access Token
def refresh_access_token(refresh_token: str):
    """
    使用 Refresh Token 生成新的 Access Token
    :param refresh_token: 传入的 Refresh Token 字符串
    :return: 新的 Access Token 字符串
    :raises HTTPException: 如果 Refresh Token 无效或过期抛出异常
    """
    try:
        # 验证并解码 Refresh Token
        decoded_token = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # 验证 token 类型是否为 'refresh'
        if decoded_token.get("type") != "refresh":
            raise HTTPException(status_code=400, detail="Invalid token type for refresh")
        
        # 获取用户数据并生成新的 Access Token
        user_data = {key: value for key, value in decoded_token.items() if key != "exp" and key != "type"}
        new_access_token = create_jwt_token(user_data)
        
        return {"access_token": new_access_token, "token_type": "bearer"}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh token has expired")
    except jwt.DecodeError:
        raise HTTPException(status_code=400, detail="Failed to decode refresh token")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=400, detail="Invalid refresh token")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

