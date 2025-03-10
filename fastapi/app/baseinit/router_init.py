from fastapi import FastAPI
from app.api.item_api import router_items
from app.api.token_api import router_token
from app.api.libitem_api import router_libitem
from app.api.libitem_api_asy import router_libitem_asy
from app.api.file_api import router_file

def routerinit(app:FastAPI):
    app.include_router(router_items)  #item
    app.include_router(router_token)  #token
    app.include_router(router_libitem)  #libitem
    app.include_router(router_libitem_asy)  #libitem_asy
    app.include_router(router_file) #file