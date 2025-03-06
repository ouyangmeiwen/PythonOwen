from app.dbmanager.dbutils import Database
from app.dbmodel.libitem_model import LibItem
from app.dtos.libitem_dto import LibitemDto
from app.dtos.libitem_input import LibitemInput
from typing import Type, TypeVar, List, Optional, Any, Tuple
from app.utils.stringutils import StringUtils
from app.utils.timeutils import TimeUtils
from app.dbmanager.dbinstance import DB_INSTANCE_ASY
from app.dtomap.libitem_map import LibitenmMap

class LibitemServiceAsy:
    def __init__(self):
        self.DB = DB_INSTANCE_ASY
        # Assuming create_tables can be asynchronous

    async def initialize(self):
        # Assuming create_tables can be asynchronous
        await self.DB.create_tables([LibItem])
    
    async def query_first(self, id: str) -> Optional[LibitemDto]:
        dynamic_kwargs = {"Id": id, "IsDeleted": 0}
        db_model = await self.DB.first_or_default(LibItem, **dynamic_kwargs)
        if db_model:
            return  LibitenmMap.model_to_dto(db_model)
        return None

    async def query_many(self, barcode: str, title: str, callno: str) -> List[LibitemDto]:
        filters = []
        if title and len(title) > 0:
            filters.append(LibItem.Title.like(f"%{title}%"))

        dynamic_kwargs = {"IsDeleted": 0}
        if barcode and len(barcode) > 0:
            dynamic_kwargs["Barcode"] = barcode
        if callno and len(callno) > 0:
            dynamic_kwargs["CallNo"] = callno

        db_models = await self.DB.where_many(LibItem, *filters, **dynamic_kwargs)
        dtos = [LibitenmMap.model_to_dto(db_model) for db_model in db_models]
        return dtos

    async def query_bypage(self, page: int, page_size: int, title: str, barcode: str) -> Tuple[List[LibitemDto], int]:
        filters = []
        if title and len(title) > 0:
            filters.append(LibItem.Title.like(f"%{title}%"))

        dynamic_kwargs = {"IsDeleted": 0}
        if barcode and len(barcode) > 0:
            dynamic_kwargs["Barcode"] = barcode

        db_list, total = await self.DB.where_bypage(LibItem,
                                                          *filters,
                                                          page=page,
                                                          page_size=page_size,
                                                          order_by="CreationTime",
                                                          ascending=True,
                                                          **dynamic_kwargs)
        dtos = [LibitenmMap.model_to_dto(item) for item in db_list] if db_list else []
        return dtos, total

    async def update(self, id: str, input: LibitemInput):
        dicts = input.__dict__.copy()
        obj = await self.DB.first_or_default(LibItem, Id=id, IsDeleted=0)
        if not obj:
            raise Exception(f"id:{id}不存在！")
        keys_to_remove = ['Id', 'CreationTime', 'CreatorUserId', 'IsDeleted', 'DeleterUserId', 'DeletionTime']
        dicts["LastModificationTime"] = TimeUtils.get_current_time()
        for key in keys_to_remove:
            dicts.pop(key, None)
        await self.DB.update(obj, **dicts)

    async def create(self, input: LibitemInput):
        input.LastModifierUserId = None
        input.LastModificationTime = None
        input.IsDeleted = False
        input.DeleterUserId = None
        input.DeletionTime = None
        input.CreationTime = TimeUtils.get_current_time()
        input.CreatorUserId = 1
        input.IsEnable = True
        obj = LibitenmMap.input_to_model(input)
        await self.DB.add(obj)

    async def delete(self, id: str, soft_delete: bool):
        if soft_delete:
            obj = await self.DB.first_or_default(LibItem, Id=id, IsDeleted=0)
            if not obj:
                raise Exception(f"id:{id}不存在！")
            dicts = {"IsDeleted": 1, "DeleterUserId": 1, "DeletionTime": TimeUtils.get_current_time()}
            await self.DB.update(obj, **dicts)
        else:
            obj = await self.DB.first_or_default(LibItem, Id=id)
            if not obj:
                raise Exception(f"id:{id}不存在！")
            await self.DB.delete(obj)
