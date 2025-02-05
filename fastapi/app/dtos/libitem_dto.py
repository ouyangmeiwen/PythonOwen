import json
from typing import Optional
from pydantic import BaseModel

class LibitemDto(BaseModel):  #带有默认值的
    Id: str = ""
    CreationTime: Optional[str] = None
    CreatorUserId: Optional[int] = None
    LastModificationTime: Optional[str] = None
    LastModifierUserId: Optional[int] = None
    IsDeleted: bool = False
    DeleterUserId: Optional[int] = None
    DeletionTime: Optional[str] = None
    InfoId: Optional[str] = None
    Title: str = ""
    Author: Optional[str] = None
    Barcode: str = ""
    IsEnable: bool = False
    CallNo: Optional[str] = None
    PreCallNo: Optional[str] = None
    CatalogCode: Optional[str] = None
    ItemState: int = 0
    PressmarkId: Optional[str] = None
    PressmarkName: Optional[str] = None
    LocationId: Optional[str] = None
    LocationName: Optional[str] = None
    BookBarcode: Optional[str] = None
    ISBN: Optional[str] = None
    PubNo: Optional[int] = None
    Publisher: Optional[str] = None
    PubDate: Optional[str] = None
    Price: Optional[str] = None
    Pages: Optional[str] = None
    Summary: Optional[str] = None
    ItemType: int = 0
    Remark: Optional[str] = None
    OriginType: int = 0
    CreateType: int = 0
    TenantId: int = 0


    def __repr__(self):
        # 获取类的所有属性和属性值
        obj_dict = vars(self)
        # 将字典转化为 JSON 格式字符串
        return json.dumps(obj_dict, ensure_ascii=False, default=str,indent=4)