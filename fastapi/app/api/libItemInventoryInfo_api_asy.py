import os
from fastapi import APIRouter, Request, Depends, HTTPException
from app.dtos.libItemInventoryInfo_dto import LibItemInventoryInfoDto
from app.dtos.libItemInventoryInfo_Input import LibItemInventoryInfoInput
from app.dtos.base_dto import Result
from app.middleware.validation import verify_token, verify_authorization
from app.utils.jwtutils import *
from app.middleware.rate_limit_middleware import *
from app.service.libItemInventoryInfo_service_asy import LibItemInventoryInfoServiceAsy
from app.utils.loggerutils import logger

# 创建路由实例
router_libiteminventoryinfo_asy = APIRouter()
libitemservice = LibItemInventoryInfoServiceAsy()

@router_libiteminventoryinfo_asy.get("/libiteminventoryinfo_asy", tags=["libiteminventoryinfo_asy"])
async def query(request: Request,
                id: str,  # 非空校验 不允许空值
                token: str = Depends(verify_authorization)):
    """
    **GET** 请求，通过id获取数据
    """
    try:
        result = await libitemservice.query_first(id=id)
        return Result.success_result(data=result, message="query success")
    except Exception as e:
        # 返回异常的详细信息
        logger.error(str(e))
        return Result.error_result(message=f"query failed: {str(e)}")


# GET 请求示例 /libiteminventoryinfo_asy/list?query_many=1111
@router_libiteminventoryinfo_asy.get("/libiteminventoryinfo_asy/query_many", tags=["libiteminventoryinfo_asy"])
async def query_many(request: Request,
                    barcode: str = None,  # 非空校验 允许空值
                    title: str = None,    # 非空校验 允许空值
                    callno: str = None,   # 非空校验 允许空值
                    token: str = Depends(verify_authorization)):
    """
    **GET** 请求，通过barcode, title, callno 获取数据
    """
    try:
        if (barcode and len(barcode) > 0) or (title and len(title) > 0) or (callno and len(callno) > 0):
            result = await libitemservice.query_many(barcode, title, callno)
            return Result.success_result(data=result, message="query success")
        else:
            return Result.error_result(message="查询参数不能全部是空的")
    except Exception as e:
        # 返回异常的详细信息
        logger.error(str(e))
        return Result.error_result(message=f"query failed: {str(e)}")


# GET 请求示例 /libiteminventoryinfo_asy/list?page=1&page_size=10&title=abc
@router_libiteminventoryinfo_asy.get("/libiteminventoryinfo_asy/query_bypage", tags=["libiteminventoryinfo_asy"])
async def query_bypage(request: Request,
                 page: int = 1,
                 page_size: int = 10,
                 title: str = None,
                 barcode: str = None,
                 token: str = Depends(verify_authorization)):
    """
    **GET** 请求，批量获取数据
    """
    try:
        db_list, total = await libitemservice.query_bypage(page=page, page_size=page_size, title=title, barcode=barcode)
        return Result.success_result(data={"total": total, "items": db_list}, message="list success")
    except Exception as e:
        # 返回异常的详细信息
        logger.error(str(e))
        return Result.error_result(message=f"list failed: {str(e)}")


# POST 请求示例
@router_libiteminventoryinfo_asy.post("/libiteminventoryinfo_asy", tags=["libiteminventoryinfo_asy"])
async def create(input: LibItemInventoryInfoInput, request: Request, token: str = Depends(verify_authorization)):
    """
    **POST** 请求，创建数据
    """
    try:
        await libitemservice.create(input)
        return Result.success_result(message="create success")
    except Exception as e:
        # 返回异常的详细信息
        logger.error(str(e))
        return Result.error_result(message=f"create failed: {str(e)}")


# PUT 请求示例 {id} 必须放第一个参数
@router_libiteminventoryinfo_asy.put("/libiteminventoryinfo_asy/{id}", tags=["libiteminventoryinfo_asy"])
async def update(id: str,
                 input: LibItemInventoryInfoInput,
                 request: Request,
                 token: str = Depends(verify_authorization)):
    """
    **PUT** 请求，更新数据
    """
    try:
        await libitemservice.update(id=id, input=input)
        return Result.success_result(message="update success")
    except Exception as e:
        # 返回异常的详细信息
        logger.error(str(e))
        return Result.error_result(message=f"update failed: {str(e)}")


# DELETE 请求示例 {id} 必须放第一个参数
@router_libiteminventoryinfo_asy.delete("/libiteminventoryinfo_asy/{id}", tags=["libiteminventoryinfo_asy"])
async def delete(id: str,
                 request: Request,
                 token: str = Depends(verify_authorization)):
    """
    **DELETE** 请求，删除数据
    """
    try:
        await libitemservice.delete(id=id)
        return Result.success_result(message="delete success")
    except Exception as e:
        # 返回异常的详细信息
        logger.error(str(e))
        return Result.error_result(message=f"delete failed: {str(e)}")
