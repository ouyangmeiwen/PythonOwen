import json
from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class LibLayerDto(BaseModel):
    """Pydantic DTO for LibLayer（字段默认值、类型完全匹配）"""

    Id: str = ""
    CreationTime: Optional[datetime] = None
    CreatorUserId: Optional[int] = None
    LastModificationTime: Optional[datetime] = None
    LastModifierUserId: Optional[int] = None
    IsDeleted: bool = False
    DeleterUserId: Optional[int] = None
    DeletionTime: Optional[datetime] = None
    ShelfId: str = ""
    Code: Optional[str] = None
    Name: str = ""
    Tid: Optional[str] = None
    Side: str = ""
    LayerNo: int = 0
    IsEnable: bool = False
    Remark: Optional[str] = None
    TenantId: int = 0
    ItemBarcode: Optional[str] = None
    ItemCallNo: Optional[str] = None
    PreCallNo: Optional[str] = None
    Barcode: Optional[str] = None
    OriginType: Optional[int] = None

    def __repr__(self):
        # 获取类的所有属性和属性值
        obj_dict = vars(self)
        # 将字典转化为 JSON 格式字符串
        return json.dumps(obj_dict, ensure_ascii=False, default=str,indent=4)