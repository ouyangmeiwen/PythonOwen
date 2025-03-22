from app.dbmanager.dbutils import Database
from app.dbmodel.libItemInventoryInfo_modle import LibItemInventoryInfo
from app.dtos.libItemInventoryInfo_dto import LibItemInventoryInfoDto
from app.dtos.libItemInventoryInfo_Input import LibItemInventoryInfoInput
from typing import Type, TypeVar, List, Optional, Any, Tuple
from app.utils.stringutils import StringUtils
from app.utils.timeutils import TimeUtils
from app.dbmanager.dbinstance import DB_INSTANCE_ASY
from app.dtomap.libItemInventoryInfo_map import LibItemInventoryInfoMap

class LibItemInventoryInfoServiceAsy:
    def __init__(self):
        self.DB = DB_INSTANCE_ASY

    async def initialize(self):
        await self.DB.create_tables([LibItemInventoryInfo])

    async def query_first(self, id: str) -> Optional[LibItemInventoryInfoDto]:
        dynamic_kwargs = {"Id": id}
        db_model = await self.DB.first_or_default(LibItemInventoryInfo, **dynamic_kwargs)
        if db_model:
            return  LibItemInventoryInfoMap.model_to_dto(db_model)
        return None

    async def query_many(self, barcode: str, title: str, callno: str) -> List[LibItemInventoryInfoDto]:
        filters = []
        if title and len(title) > 0:
            filters.append(LibItemInventoryInfo.OCRItemTitle.like(f"%{title}%"))

        dynamic_kwargs = { }
        if barcode and len(barcode) > 0:
            dynamic_kwargs["ItemBarcode"] = barcode
        if callno and len(callno) > 0:
            dynamic_kwargs["OCRItemCallNo"] = callno

        db_models = await self.DB.where_many(LibItemInventoryInfo, *filters, **dynamic_kwargs)
        dtos = [LibItemInventoryInfoMap.model_to_dto(db_model) for db_model in db_models]
        return dtos

    async def query_bypage(self, page: int, page_size: int, title: str, barcode: str) -> Tuple[List[LibItemInventoryInfoDto], int]:
        filters = []
        if title and len(title) > 0:
            filters.append(LibItemInventoryInfo.OCRItemTitle.like(f"%{title}%"))

        dynamic_kwargs = { }
        if barcode and len(barcode) > 0:
            dynamic_kwargs["ItemBarcode"] = barcode

        db_list, total = await self.DB.where_bypage(LibItemInventoryInfo,
                                                          *filters,
                                                          page=page,
                                                          page_size=page_size,
                                                          order_by="CreationTime",
                                                          ascending=True,
                                                          **dynamic_kwargs)
        dtos = [LibItemInventoryInfoMap.model_to_dto(item) for item in db_list] if db_list else []
        return dtos, total

    async def update(self, id: str, input: LibItemInventoryInfoInput):
        dicts = input.__dict__.copy()
        obj = await self.DB.first_or_default(LibItemInventoryInfo, Id=id)
        if not obj:
            raise Exception(f"id:{id}不存在！")
        keys_to_remove = ['Id', 'CreationTime', 'CreatorUserId']
        dicts["LastModificationTime"] = TimeUtils.get_current_time()
        for key in keys_to_remove:
            dicts.pop(key, None)
        await self.DB.update(obj, **dicts)

    async def create(self, input: LibItemInventoryInfoInput):
        input.LastModifierUserId = None
        input.LastModificationTime = None
        input.CreationTime = TimeUtils.get_current_time()
        input.CreatorUserId = 1
        obj = LibItemInventoryInfoMap.input_to_model(input)
        await self.DB.add(obj)

    async def delete(self, id: str):
        obj = await self.DB.first_or_default(LibItemInventoryInfo, Id=id)
        if not obj:
            raise Exception(f"id:{id}不存在！")
        await self.DB.delete(obj)


