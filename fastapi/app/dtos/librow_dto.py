import json
from typing import Optional
from pydantic import BaseModel
from typing import List
from app.dtos.libshelf_dto import LibShelfDto
from datetime import datetime

class LibRowDto(BaseModel):
    """Pydantic DTO for LibRow（带默认值）"""

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
    CatalogCode: Optional[str] = None
    RowNo: int = 0
    RowType: int = 0
    RowUsageType: int = 0
    LocationId: Optional[str] = None
    Remark: Optional[str] = None
    TenantId: int = 0

    #关联的列集合
    Shelfs:List[LibShelfDto]=[]

    def __repr__(self):
        # 获取类的所有属性和属性值
        obj_dict = vars(self)
        # 将字典转化为 JSON 格式字符串
        return json.dumps(obj_dict, ensure_ascii=False, default=str,indent=4)
