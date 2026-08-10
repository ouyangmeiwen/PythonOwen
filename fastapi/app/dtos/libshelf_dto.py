import json
from typing import Optional
from pydantic import BaseModel
from typing import List
from app.dtos.liblayer_dto import LibLayerDto
from datetime import datetime

class LibShelfDto(BaseModel):
    """Pydantic DTO for LibShelf（含默认值）"""

    Id: str = ""
    CreationTime: Optional[datetime] = None
    CreatorUserId: Optional[int] = None
    LastModificationTime: Optional[datetime] = None
    LastModifierUserId: Optional[int] = None
    IsDeleted: bool = False
    DeleterUserId: Optional[int] = None
    DeletionTime: Optional[datetime] = None
    Code: Optional[str] = None
    Name: Optional[str] = None
    ShelfNo: int = 0
    Side: Optional[str] = None
    RowIdentity: str = ""
    RfidReaderId: Optional[str] = None
    SerialPortId: Optional[str] = None
    IsEnable: bool = False
    X1: Optional[float] = None
    Y1: Optional[float] = None
    X2: Optional[float] = None
    Y2: Optional[float] = None
    Angel: Optional[float] = None
    StructId: Optional[str] = None
    Remark: Optional[str] = None
    TenantId: int = 0
    IsBosseyed: bool = False

    # 关联的 LibLayerDto 列表
    Layers:List[LibLayerDto]=[]

    def __repr__(self):
        # 获取类的所有属性和属性值
        obj_dict = vars(self)
        # 将字典转化为 JSON 格式字符串
        return json.dumps(obj_dict, ensure_ascii=False, default=str,indent=4)
