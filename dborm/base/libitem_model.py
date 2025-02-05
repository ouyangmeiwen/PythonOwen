import json
from sqlalchemy import Column, Integer, String, Unicode, BigInteger, SmallInteger, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base

# 假设 Base 在 base.basemodel 中已经定义
from base.basemodel import Base

class LibItem(Base):
    __tablename__ = 'LibItem'

    # 字段定义
    Id = Column(String(32), primary_key=True, index=True, nullable=False)
    CreationTime = Column(DateTime, nullable=True)
    CreatorUserId = Column(BigInteger, nullable=True)
    LastModificationTime = Column(DateTime, nullable=True)
    LastModifierUserId = Column(BigInteger, nullable=True)
    IsDeleted = Column(Boolean, nullable=False)
    DeleterUserId = Column(BigInteger, nullable=True)
    DeletionTime = Column(DateTime, nullable=True)
    InfoId = Column(String(32), nullable=True)
    Title = Column(Unicode(256), nullable=False)
    Author = Column(Unicode(256), nullable=True)
    Barcode = Column(String(32), nullable=False)
    IsEnable = Column(Boolean, nullable=False)
    CallNo = Column(Unicode(64), nullable=True)
    PreCallNo = Column(Unicode(64), nullable=True)
    CatalogCode = Column(String(32), nullable=True)
    ItemState = Column(Integer, nullable=False)  # 用数字表示状态
    PressmarkId = Column(String(32), nullable=True)
    PressmarkName = Column(Unicode(64), nullable=True)
    LocationId = Column(String(32), nullable=True)
    LocationName = Column(Unicode(128), nullable=True)
    BookBarcode = Column(String(32), nullable=True)
    ISBN = Column(String(32), nullable=True)
    PubNo = Column(SmallInteger, nullable=True)
    Publisher = Column(Unicode(512), nullable=True)
    PubDate = Column(String(32), nullable=True)
    Price = Column(String(32), nullable=True)
    Pages = Column(String(32), nullable=True)
    Summary = Column(Unicode(4000), nullable=True)
    ItemType = Column(Integer, nullable=False)
    Remark = Column(Unicode(256), nullable=True)
    OriginType = Column(Integer, nullable=False)  # 用数字表示来源类型
    CreateType = Column(Integer, nullable=False)  # 用数字表示创建类型
    TenantId = Column(Integer, nullable=False)

    def __repr__(self):
        # 获取类的所有属性和属性值
        obj_dict = vars(self)
        # 将字典转化为 JSON 格式字符串
        return json.dumps(obj_dict, ensure_ascii=False, default=str,indent=4)
