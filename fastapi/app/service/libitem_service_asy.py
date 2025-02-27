from app.dbmanager.dbutils import Database
from app.dbmodel.libitem_model import LibItem
from app.dtos.libitem_dto import LibitemDto
from app.dtos.libitem_input import LibitemInput
from typing import Type, TypeVar, List, Optional, Any, Tuple
from app.utils.stringutils import StringUtils
from app.utils.timeutils import TimeUtils
from app.dbmanager.dbinstance import DB_INSTANCE_ASY

class LibitemServiceAsy:
    def __init__(self):
        self.DB = DB_INSTANCE_ASY
        # Assuming create_tables can be asynchronous

    async def initialize(self):
        # Assuming create_tables can be asynchronous
        await self.DB.create_tables([LibItem])
        
    async def model_to_dto(self, db_model: LibItem) -> LibitemDto:
        dto = LibitemDto(Id=db_model.Id)
        dto.CreationTime = db_model.CreationTime
        dto.CreatorUserId = db_model.CreatorUserId
        dto.LastModificationTime = db_model.LastModificationTime
        dto.IsDeleted = StringUtils.to_bool(db_model.IsDeleted)  # db is int, dto is bool
        dto.DeleterUserId = db_model.DeleterUserId
        dto.DeletionTime = db_model.DeletionTime
        dto.InfoId = db_model.InfoId
        dto.Title = db_model.Title
        dto.Author = db_model.Author
        dto.Barcode = db_model.Barcode
        dto.IsEnable = StringUtils.to_bool(db_model.IsEnable)  # db is int, dto is bool
        dto.CallNo = db_model.CallNo
        dto.PreCallNo = db_model.PreCallNo
        dto.CatalogCode = db_model.CatalogCode
        dto.ItemState = db_model.ItemState
        dto.PressmarkId = db_model.PressmarkId
        dto.PressmarkName = db_model.PressmarkName
        dto.LocationId = db_model.LocationId
        dto.LocationName = db_model.LocationName
        dto.BookBarcode = db_model.BookBarcode
        dto.ISBN = db_model.ISBN
        dto.PubNo = db_model.PubNo
        dto.Publisher = db_model.Publisher
        dto.PubDate = db_model.PubDate
        dto.Price = db_model.Price
        dto.Pages = db_model.Pages
        dto.Summary = db_model.Summary
        dto.ItemType = db_model.ItemType
        dto.Remark = db_model.Remark
        dto.OriginType = db_model.OriginType
        dto.CreateType = db_model.CreateType
        dto.TenantId = db_model.TenantId
        return dto

    async def input_to_model(self, input: LibitemInput) -> LibItem:
        dt_model = LibItem(Id=input.Id)
        dt_model.CreationTime = input.CreationTime
        dt_model.CreatorUserId = input.CreatorUserId
        dt_model.LastModificationTime = input.LastModificationTime
        dt_model.IsDeleted = 1 if input.IsDeleted else 0
        dt_model.DeleterUserId = input.DeleterUserId
        dt_model.DeletionTime = input.DeletionTime
        dt_model.InfoId = input.InfoId
        dt_model.Title = input.Title
        dt_model.Author = input.Author
        dt_model.Barcode = input.Barcode
        dt_model.IsEnable = 1 if input.IsEnable else 0
        dt_model.CallNo = input.CallNo
        dt_model.PreCallNo = input.PreCallNo
        dt_model.CatalogCode = input.CatalogCode
        dt_model.ItemState = input.ItemState
        dt_model.PressmarkId = input.PressmarkId
        dt_model.PressmarkName = input.PressmarkName
        dt_model.LocationId = input.LocationId
        dt_model.LocationName = input.LocationName
        dt_model.BookBarcode = input.BookBarcode
        dt_model.ISBN = input.ISBN
        dt_model.PubNo = input.PubNo
        dt_model.Publisher = input.Publisher
        dt_model.PubDate = input.PubDate
        dt_model.Price = input.Price
        dt_model.Pages = input.Pages
        dt_model.Summary = input.Summary
        dt_model.ItemType = input.ItemType
        dt_model.Remark = input.Remark
        dt_model.OriginType = input.OriginType
        dt_model.CreateType = input.CreateType
        dt_model.TenantId = input.TenantId
        return dt_model

    async def query_first(self, id: str) -> Optional[LibitemDto]:
        dynamic_kwargs = {"Id": id, "IsDeleted": 0}
        db_model = await self.DB.first_or_default(LibItem, **dynamic_kwargs)
        if db_model:
            return await self.model_to_dto(db_model)
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

        db_models = await self.DB.list_many(LibItem, *filters, **dynamic_kwargs)
        dtos = [await self.model_to_dto(db_model) for db_model in db_models]
        return dtos

    async def getall(self, page: int, page_size: int, title: str, barcode: str) -> Tuple[List[LibitemDto], int]:
        filters = []
        if title and len(title) > 0:
            filters.append(LibItem.Title.like(f"%{title}%"))

        dynamic_kwargs = {"IsDeleted": 0}
        if barcode and len(barcode) > 0:
            dynamic_kwargs["Barcode"] = barcode

        db_list, total = await self.DB.list_dicts_bypage(LibItem,
                                                          *filters,
                                                          page=page,
                                                          page_size=page_size,
                                                          order_by="CreationTime",
                                                          ascending=True,
                                                          **dynamic_kwargs)
        dtos = [await self.model_to_dto(item) for item in db_list] if db_list else []
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
        obj = await self.input_to_model(input)
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
