import os
from fastapi import APIRouter, Request, Depends, HTTPException
from app.dtos.libitem_dto import LibitemDto
from app.dtos.libitem_input import LibitemInput
from app.dtos.base_dto import Result
from app.middleware.validation import verify_token, verify_authorization
from app.utils.jwtutils import *
from app.middleware.rate_limit_middleware import *
from app.service.librow_service import LibRowServiceAsync
from app.utils.loggerutils import logger

# 创建路由实例
router_librow_asy = APIRouter()

librowserviceAsy = LibRowServiceAsync()

@router_librow_asy.get("/librow_asy/query_many", tags=["librow_asy"])
async def query_many(request: Request,
                    rowno: int = None,  # 非空校验 允许空值
                    token: str = Depends(verify_authorization)):
    try:
        result = await librowserviceAsy.query_many(rowno)
        return Result.success_result(data=result, message="query success")
    except Exception as e:
        # 返回异常的详细信息
        logger.error(str(e))
        return Result.error_result(message=f"query failed: {str(e)}")
