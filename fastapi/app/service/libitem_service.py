from app.dbmanager.dbutils import Database
from app.dbmodel.libitem_model import LibItem
from app.dtos.libitem_dto import LibitemDto
from app.dtos.libitem_input import LibitemInput
from typing import Type, TypeVar, List, Optional,Any
from app.utils.stringutils import StringUtils
from typing import Type, TypeVar, List, Optional,Any ,Tuple
from app.utils.timeutils import TimeUtils
from app.dbmanager.dbinstance import DB_INSTANCE
from app.dtomap.libitem_map import LibitenmMap
class LibitemService:
    def __init__(self):
        self.DB=DB_INSTANCE
        self.DB.create_tables([LibItem])

    def initialize(self):
        self.DB.create_tables([LibItem])
        
    #增加sessin销毁  单例是不需要销毁的
    # def __del__(self):
    #     self.DB.close()

    def query_first(self,id:str)->Optional[LibitemDto]:
        dynamic_kwargs = {}
        dynamic_kwargs["Id"] = id 
        dynamic_kwargs["IsDeleted"] = 0

        db_model=self.DB.first_or_default(LibItem,**dynamic_kwargs)
        if db_model:
            return LibitenmMap.model_to_dto(db_model)
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
            
        db_models=self.DB.where_many(LibItem,*filters,**dynamic_kwargs)
        dtos:List[LibitemDto]=[]
        for db_model in db_models:
            dto=LibitenmMap.model_to_dto(db_model)
            dtos.append(dto)
        return dtos


    def query_bypage(self,page:int,page_size:int,title:str,barcode:str)-> Tuple[List[LibitemDto], int]:
        filters = []
        if title and len(title) > 0:  # 检查 title 是否非空
            filters.append(LibItem.Title.like(f"%{title}%"))  # 添加模糊匹配过滤条件

        dynamic_kwargs = {}
        dynamic_kwargs["IsDeleted"] = 0

        if barcode and len(barcode) > 0:
            dynamic_kwargs["Barcode"] = barcode  # 如果 title 不为空，加入到 kwargs 中

        db_list,total=self.DB.where_bypage(LibItem,
                                        *filters,  # 动态传递过滤条件
                                        page=page,
                                        page_size=page_size,
                                        order_by="CreationTime",
                                        ascending=True,
                                        **dynamic_kwargs)
        if db_list:
            dtos:List[LibitemDto]=[]
            for item in db_list:
                dto=LibitenmMap.model_to_dto(item)
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
        obj=LibitenmMap.input_to_model(input)
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