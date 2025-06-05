from sqlalchemy import Column, String, DateTime, BigInteger, Integer, SmallInteger
from sqlalchemy.dialects.mysql import TINYINT
from app.dbmodel.base_model import Base  # 你的 Base 模型应在此处定义
import json


class LibLayer(Base):
    __tablename__ = 'LibLayer'

    Id = Column(String(32), primary_key=True, index=True, nullable=False)
    CreationTime = Column(DateTime, nullable=True)
    CreatorUserId = Column(BigInteger, nullable=True)
    LastModificationTime = Column(DateTime, nullable=True)
    LastModifierUserId = Column(BigInteger, nullable=True)
    IsDeleted = Column(TINYINT(1), nullable=False)
    DeleterUserId = Column(BigInteger, nullable=True)
    DeletionTime = Column(DateTime, nullable=True)
    ShelfId = Column(String(32), nullable=False)
    Code = Column(String(32), nullable=True)
    Name = Column(String(128), nullable=False)
    Tid = Column(String(32), nullable=True)
    Side = Column(String(32), nullable=False)
    LayerNo = Column(SmallInteger, nullable=False)  # tinyint unsigned → SmallInteger
    IsEnable = Column(TINYINT(1), nullable=False)
    Remark = Column(String(256), nullable=True)
    TenantId = Column(Integer, nullable=False)
    ItemBarcode = Column(String(32), nullable=True)
    ItemCallNo = Column(String(64), nullable=True)
    PreCallNo = Column(String(64), nullable=True)
    Barcode = Column(String(32), nullable=True)
    OriginType = Column(SmallInteger, nullable=True)



    def __repr__(self):
        obj_dict = vars(self)
        return json.dumps(obj_dict, ensure_ascii=False, default=str, indent=4)