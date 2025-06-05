from sqlalchemy import Column, String, DateTime, BigInteger, Integer, DECIMAL
from sqlalchemy.dialects.mysql import TINYINT
from app.dbmodel.base_model import Base  # 假设 Base 已定义在此处
import json

class LibShelf(Base):
    __tablename__ = 'LibShelf'

    Id = Column(String(32), primary_key=True, index=True, nullable=False)
    CreationTime = Column(DateTime, nullable=True)
    CreatorUserId = Column(BigInteger, nullable=True)
    LastModificationTime = Column(DateTime, nullable=True)
    LastModifierUserId = Column(BigInteger, nullable=True)
    IsDeleted = Column(TINYINT(1), nullable=False)
    DeleterUserId = Column(BigInteger, nullable=True)
    DeletionTime = Column(DateTime, nullable=True)
    Code = Column(String(32), nullable=True)
    Name = Column(String(128), nullable=True)
    ShelfNo = Column(Integer, nullable=False)
    Side = Column(String(32), nullable=True)
    RowIdentity = Column(String(32), nullable=False, default='')
    RfidReaderId = Column(String(32), nullable=True)
    SerialPortId = Column(String(32), nullable=True)
    IsEnable = Column(TINYINT(1), nullable=False)
    X1 = Column(DECIMAL(7, 2), nullable=True)
    Y1 = Column(DECIMAL(7, 2), nullable=True)
    X2 = Column(DECIMAL(7, 2), nullable=True)
    Y2 = Column(DECIMAL(7, 2), nullable=True)
    Angel = Column(DECIMAL(7, 2), nullable=True)
    StructId = Column(String(255), nullable=True)
    Remark = Column(String(256), nullable=True)
    TenantId = Column(Integer, nullable=False)
    IsBosseyed = Column(TINYINT(1), nullable=False, default=0)


    def __repr__(self):
            obj_dict = vars(self)
            return json.dumps(obj_dict, ensure_ascii=False, default=str, indent=4)