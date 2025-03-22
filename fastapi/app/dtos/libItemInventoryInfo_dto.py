import json
from pydantic import BaseModel
from typing import Optional

class LibItemInventoryInfoDto(BaseModel):
    Id: str
    CreationTime: Optional[str] = None
    CreatorUserId: Optional[int] = None
    LastModificationTime: Optional[str] = None
    LastModifierUserId: Optional[int] = None
    ItemTid: Optional[str] = None
    ItemEpc: Optional[str] = None
    LayerId: Optional[str] = None
    Antenna: Optional[str] = None
    InventoryState: int
    ItemBarcode: Optional[str] = None
    Remark: Optional[str] = None
    TenantId: int
    LayerCode: Optional[str] = None
    ExceptionMsg: Optional[str] = None
    OCRItemAuthor: Optional[str] = None
    OCRItemCallNo: Optional[str] = None
    OCRItemISBN: Optional[str] = None
    OCRItemPublisher: Optional[str] = None
    OCRItemTitle: Optional[str] = None
    OriginType: Optional[int] = None
    LayerName: Optional[str] = None
    LocLayerCode: Optional[str] = None
    LocLayerId: Optional[str] = None
    LocLayerName: Optional[str] = None
    OffShelfTime: Optional[str] = None

    def __repr__(self):
        return json.dumps(self.dict(), ensure_ascii=False, indent=4, default=str)
