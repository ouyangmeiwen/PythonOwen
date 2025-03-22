import json
from sqlalchemy import Column, Integer, String, Unicode, BigInteger, SmallInteger, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.mysql import TINYINT
from app.dbmodel.base_model import Base  # 假设 Base 已在 base_model 定义

class LibItemInventoryInfo(Base):
    __tablename__ = 'LibItemInventoryInfo'

    Id = Column(String(32), primary_key=True, index=True, nullable=False)
    CreationTime = Column(DateTime, nullable=True)
    CreatorUserId = Column(BigInteger, nullable=True)
    LastModificationTime = Column(DateTime, nullable=True)
    LastModifierUserId = Column(BigInteger, nullable=True)
    ItemTid = Column(String(32), nullable=True)
    ItemEpc = Column(String(32), nullable=True)
    LayerId = Column(String(32), nullable=True)
    Antenna = Column(Unicode(256), nullable=True)
    InventoryState =Column(Integer, nullable=False) 
    ItemBarcode = Column(String(32), nullable=True)
    Remark = Column(Unicode(256), nullable=True)
    TenantId = Column(Integer, nullable=False)
    LayerCode = Column(String(32), nullable=True)
    ExceptionMsg = Column(Unicode(256), nullable=True)
    OCRItemAuthor = Column(Unicode(256), nullable=True)
    OCRItemCallNo = Column(Unicode(64), nullable=True)
    OCRItemISBN = Column(String(32), nullable=True)
    OCRItemPublisher = Column(Unicode(512), nullable=True)
    OCRItemTitle = Column(Unicode(256), nullable=True)
    OriginType = Column(TINYINT(unsigned=True), nullable=True)
    LayerName = Column(Unicode(32), nullable=True)
    LocLayerCode = Column(String(32), nullable=True)
    LocLayerId = Column(String(32), nullable=True)
    LocLayerName = Column(Unicode(32), nullable=True)
    OffShelfTime = Column(DateTime, nullable=True)

    def __repr__(self):
        obj_dict = {col.name: getattr(self, col.name) for col in self.__table__.columns}
        return json.dumps(obj_dict, ensure_ascii=False, default=str, indent=4)
