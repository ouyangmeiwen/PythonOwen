import json
from sqlalchemy import Column, Integer, String, Unicode, BigInteger, SmallInteger, DateTime
from sqlalchemy.dialects.mysql import TINYINT
from app.dbmodel.base_model import Base  # 假设 Base 已定义

class LibRow(Base):
    """SQLAlchemy 模型 - LibRow 表"""
    __tablename__ = 'LibRow'

    # 字段定义
    Id = Column(String(32), primary_key=True, index=True, nullable=False)
    CreationTime = Column(DateTime, nullable=True)
    CreatorUserId = Column(BigInteger, nullable=True)
    LastModificationTime = Column(DateTime, nullable=True)
    LastModifierUserId = Column(BigInteger, nullable=True)
    IsDeleted = Column(TINYINT(1), nullable=False)  # bool 用 TINYINT(1)
    DeleterUserId = Column(BigInteger, nullable=True)
    DeletionTime = Column(DateTime, nullable=True)
    Code = Column(String(32), nullable=True)
    Name = Column(Unicode(128), nullable=True)
    CatalogCode = Column(String(32), nullable=True)
    RowNo = Column(Integer, nullable=False)
    RowType = Column(SmallInteger, nullable=False)         # tinyint unsigned -> SmallInteger
    RowUsageType = Column(SmallInteger, nullable=False)    # tinyint unsigned -> SmallInteger
    LocationId = Column(String(32), nullable=True)
    Remark = Column(Unicode(256), nullable=True)
    TenantId = Column(Integer, nullable=False)

    def __repr__(self):
        obj_dict = vars(self)
        return json.dumps(obj_dict, ensure_ascii=False, default=str, indent=4)
