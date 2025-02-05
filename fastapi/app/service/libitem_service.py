from app.dbmanager.dbutils import Database
from app.dbmodel.libitem_model import LibItem
from app.dtos.libitem_dto import LibitemDto
from app.dtos.libitem_input import LibitemInput
from typing import Type, TypeVar, List, Optional,Any
from app.utils.stringutils import StringUtils
from typing import Type, TypeVar, List, Optional,Any ,Tuple
from app.utils.timeutils import TimeUtils
from app.dbmanager.dbinstance import DB_INSTANCE
class LibitemService:
    def __init__(self):
        self.DB=DB_INSTANCE
        self.DB.create_tables([LibItem])

    #增加sessin销毁  单例是不需要销毁的
    # def __del__(self):
    #     self.DB.close()

    def model_to_dto(self,db_model:LibItem)->LibitemDto:
        dto=LibitemDto(Id=db_model.Id)
        dto.CreationTime=db_model.CreationTime
        dto.CreatorUserId=db_model.CreatorUserId
        dto.LastModificationTime=db_model.LastModificationTime
        dto.IsDeleted=StringUtils.to_bool(db_model.IsDeleted)   #db是int，dto 是bool
        dto.DeleterUserId=db_model.DeleterUserId
        dto.DeletionTime=db_model.DeletionTime
        dto.InfoId=db_model.InfoId
        dto.Title=db_model.Title
        dto.Author=db_model.Author
        dto.Barcode=db_model.Barcode
        dto.IsEnable=StringUtils.to_bool(db_model.IsEnable)     #db是int，dto 是bool
        dto.CallNo=db_model.CallNo
        dto.PreCallNo=db_model.PreCallNo
        dto.CatalogCode=db_model.CatalogCode
        dto.ItemState=db_model.ItemState
        dto.PressmarkId=db_model.PressmarkId
        dto.PressmarkName=db_model.PressmarkName
        dto.LocationId=db_model.LocationId
        dto.LocationName=db_model.LocationName
        dto.BookBarcode=db_model.BookBarcode
        dto.ISBN=db_model.ISBN
        dto.PubNo=db_model.PubNo
        dto.Publisher=db_model.Publisher
        dto.PubDate=db_model.PubDate
        dto.Price=db_model.Price
        dto.Pages=db_model.Pages
        dto.Summary=db_model.Summary
        dto.ItemType=db_model.ItemType
        dto.Remark=db_model.Remark
        dto.OriginType=db_model.OriginType
        dto.CreateType=db_model.CreateType
        dto.TenantId=db_model.TenantId
        return dto



    def input_to_model(self,input:LibitemInput)->LibItem:
        dt_model=LibItem(Id=input.Id)
        dt_model.CreationTime=input.CreationTime
        dt_model.CreatorUserId=input.CreatorUserId
        dt_model.LastModificationTime=input.LastModificationTime
        dt_model.IsDeleted=1 if input.IsDeleted else 0
        dt_model.DeleterUserId=input.DeleterUserId
        dt_model.DeletionTime=input.DeletionTime
        dt_model.InfoId=input.InfoId
        dt_model.Title=input.Title
        dt_model.Author=input.Author
        dt_model.Barcode=input.Barcode
        dt_model.IsEnable=1 if input.IsEnable else 0
        dt_model.CallNo=input.CallNo
        dt_model.PreCallNo=input.PreCallNo
        dt_model.CatalogCode=input.CatalogCode
        dt_model.ItemState=input.ItemState
        dt_model.PressmarkId=input.PressmarkId
        dt_model.PressmarkName=input.PressmarkName
        dt_model.LocationId=input.LocationId
        dt_model.LocationName=input.LocationName
        dt_model.BookBarcode=input.BookBarcode
        dt_model.ISBN=input.ISBN
        dt_model.PubNo=input.PubNo
        dt_model.Publisher=input.Publisher
        dt_model.PubDate=input.PubDate
        dt_model.Price=input.Price
        dt_model.Pages=input.Pages
        dt_model.Summary=input.Summary
        dt_model.ItemType=input.ItemType
        dt_model.Remark=input.Remark
        dt_model.OriginType=input.OriginType
        dt_model.CreateType=input.CreateType
        dt_model.TenantId=input.TenantId
        return dt_model
    


    def query_first(self,id:str)->Optional[LibitemDto]:
        dynamic_kwargs = {}
        dynamic_kwargs["Id"] = id 
        dynamic_kwargs["IsDeleted"] = 0

        db_model=self.DB.first_or_default(LibItem,**dynamic_kwargs)
        if db_model:
            return self.model_to_dto(db_model)
        else:
            return None
    
    def query_many(self,barcode:str,title:str,callno:str)->List[LibitemDto]:

        filters = []
        if title and len(title) > 0:  # 检查 title 是否非空
            filters.append(LibItem.Title.like(f"%{title}%"))  # 添加模糊匹配过滤条件

        dynamic_kwargs = {}
        dynamic_kwargs["IsDeleted"] = 0
        if barcode and len(barcode) > 0:
            dynamic_kwargs["Barcode"] =barcode
        if callno and len(callno) > 0:
            dynamic_kwargs["CallNo"] = callno
            
        db_models=self.DB.list_many(LibItem,*filters,**dynamic_kwargs)
        dtos:List[LibitemDto]=[]
        for db_model in db_models:
            dto=self.model_to_dto(db_model)
            dtos.append(dto)
        return dtos


    def getall(self,page:int,page_size:int,title:str,barcode:str)-> Tuple[List[LibitemDto], int]:
        filters = []
        if title and len(title) > 0:  # 检查 title 是否非空
            filters.append(LibItem.Title.like(f"%{title}%"))  # 添加模糊匹配过滤条件

        dynamic_kwargs = {}
        dynamic_kwargs["IsDeleted"] = 0

        if barcode and len(barcode) > 0:
            dynamic_kwargs["Barcode"] = barcode  # 如果 title 不为空，加入到 kwargs 中

        db_list,total=self.DB.list_dicts_bypage(LibItem,
                                        *filters,  # 动态传递过滤条件
                                        page=page,
                                        page_size=page_size,
                                        order_by="CreationTime",
                                        ascending=True,
                                        **dynamic_kwargs)
        if db_list:
            dtos:List[LibitemDto]=[]
            for item in db_list:
                dto=self.model_to_dto(item)
                dtos.append(dto)
            return dtos,total
        else:
            return None


    def update(self,id:str,input:LibitemInput):
        # 将 dto 转换为字典
        dicts = input.__dict__.copy()  # 复制字典，避免直接修改 dto.__dict__
        obj=self.DB.first_or_default(LibItem,Id=id,IsDeleted=0)
        if not obj:
            raise Exception(f"id:{id}不存在！") 
        # 移除特定字段
        keys_to_remove = ['Id'
                          , 'CreationTime'
                          , 'CreatorUserId'
                          , 'IsDeleted'
                          , 'DeleterUserId'
                          , 'DeletionTime']  # 需要移除的字段
        dicts["LastModificationTime"]=TimeUtils.get_current_time()
        for key in keys_to_remove:
            dicts.pop(key, None)  # 使用 pop 并忽略不存在的键
        self.DB.update(obj,**dicts)

    def create(self,input:LibitemInput):
        input.LastModifierUserId=None
        input.LastModificationTime=None
        input.IsDeleted=False
        input.DeleterUserId=None
        input.DeletionTime=None
        input.CreationTime=TimeUtils.get_current_time()
        input.CreatorUserId=1
        input.IsEnable=True
        obj=self.input_to_model(input)
        self.DB.add(obj)


    def delete(self,id:str,soft_delete:bool):
        if soft_delete:
            obj=self.DB.first_or_default(LibItem,Id=id,IsDeleted=0)
            if not obj:
                raise Exception(f"id:{id}不存在！") 
            dicts=dict()
            dicts["IsDeleted"]=1
            dicts["DeleterUserId"]=1
            dicts["DeletionTime"]=TimeUtils.get_current_time()
            self.DB.update(obj,**dicts)
        else:
            obj=self.DB.first_or_default(LibItem,Id=id)
            if not obj:
                raise Exception(f"id:{id}不存在！") 
            self.DB.delete(obj)