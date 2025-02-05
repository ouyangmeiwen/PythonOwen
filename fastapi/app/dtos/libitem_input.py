# models.py
import json
from pydantic import BaseModel
from typing import Optional

class LibitemInput(BaseModel):
    Id: str
    CreationTime: Optional[str]
    CreatorUserId: Optional[int]
    LastModificationTime: Optional[str]
    LastModifierUserId: Optional[int]
    IsDeleted: bool
    DeleterUserId: Optional[int]
    DeletionTime: Optional[str]
    InfoId: Optional[str]
    Title: str
    Author: Optional[str]
    Barcode: str
    IsEnable: bool
    CallNo: Optional[str]
    PreCallNo: Optional[str]
    CatalogCode: Optional[str]
    ItemState: int
    PressmarkId: Optional[str]
    PressmarkName: Optional[str]
    LocationId: Optional[str]
    LocationName: Optional[str]
    BookBarcode: Optional[str]
    ISBN: Optional[str]
    PubNo: Optional[int]
    Publisher: Optional[str]
    PubDate: Optional[str]
    Price: Optional[str]
    Pages: Optional[str]
    Summary: Optional[str]
    ItemType: int
    Remark: Optional[str]
    OriginType: int
    CreateType: int
    TenantId: int


    def __repr__(self):
        # 获取类的所有属性和属性值
        obj_dict = vars(self)
        # 将字典转化为 JSON 格式字符串
        return json.dumps(obj_dict, ensure_ascii=False, default=str,indent=4)