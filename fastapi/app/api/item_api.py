import os
from fastapi import APIRouter, Request, Depends,HTTPException
from app.dtos.item_dto import ItemDto
from app.middleware.validation import verify_token,verify_authorization

# 创建路由实例
router_items = APIRouter()


# http://127.0.0.1:8000/items/1
# GET 请求示例
@router_items.get("/items/{item_id}", tags=["items"])
def read_item(item_id: int, request: Request, q: str = None, token: str = Depends(verify_authorization)):
    """
    **GET** 请求，获取商品信息
    - `item_id` (int): 商品 ID，路径参数
    - `q` (str, optional): 查询参数（可选）
    - `request` (Request): 请求对象，包含请求头等信息
    - `token` (str): 请求中的认证 token（由 verify_token 验证）
    """
    print(f"Item ID: {item_id}, Query: {q}")
    print(f"Headers: {request.headers}")
    return {"item_id": item_id, "q": q}

# POST 请求示例
@router_items.post("/items/", tags=["items"])
async def create_item(item: ItemDto, request: Request, token: str = Depends(verify_authorization)):
    """
    **POST** 请求，创建商品
    - `item` (Item): 商品信息，来自请求体（JSON）
    - `request` (Request): 请求对象，包含请求头等信息
    - `token` (str): 请求中的认证 token（由 verify_token 验证）
    """
    print(f"Request Body: {item.model_dump()}")
    print(f"Headers: {request.headers}")
    return {"name": item.name, "price": item.price, "tax": item.tax}

# PUT 请求示例
@router_items.put("/items/{item_id}", tags=["items"])
async def update_item(item_id: int, item: ItemDto, request: Request, token: str = Depends(verify_authorization)):
    """
    **PUT** 请求，更新商品信息
    - `item_id` (int): 商品 ID，路径参数
    - `item` (Item): 更新后的商品信息，来自请求体（JSON）
    - `request` (Request): 请求对象，包含请求头等信息
    - `token` (str): 请求中的认证 token（由 verify_token 验证）
    """
    print(f"Item ID: {item_id}")
    print(f"Request Body: {item.model_dump()}")
    print(f"Headers: {request.headers}")
    return {"item_id": item_id, "name": item.name, "price": item.price, "tax": item.tax}

# DELETE 请求示例
@router_items.delete("/items/{item_id}", tags=["items"])
async def delete_item(item_id: int, request: Request, token: str = Depends(verify_authorization)):
    """
    **DELETE** 请求，删除商品
    - `item_id` (int): 商品 ID，路径参数
    - `request` (Request): 请求对象，包含请求头等信息
    - `token` (str): 请求中的认证 token（由 verify_token 验证）
    """
    print(f"Item ID to delete: {item_id}")
    print(f"Headers: {request.headers}")
    return {"message": f"Item {item_id} has been deleted"}

# PATCH 请求示例
@router_items.patch("/items/{item_id}", tags=["items"])
async def partial_update_item(item_id: int, item: ItemDto, request: Request, token: str = Depends(verify_authorization)):
    """
    **PATCH** 请求，部分更新商品信息
    - `item_id` (int): 商品 ID，路径参数
    - `item` (Item): 要更新的字段，来自请求体（JSON）
    - `request` (Request): 请求对象，包含请求头等信息
    - `token` (str): 请求中的认证 token（由 verify_token 验证）
    """
    print(f"Item ID: {item_id}")
    print(f"Request Body: {item.model_dump()}")
    print(f"Headers: {request.headers}")
    return {"item_id": item_id, "name": item.name, "price": item.price, "tax": item.tax}
