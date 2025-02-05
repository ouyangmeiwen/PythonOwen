from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Unicode
from base.basemodel import Base


# 定义 User 模型
class User_Mysql(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(Unicode(100), unique=False)  # 支持 Unicode 字符
    email = Column(String(255), unique=False)  # 使用合适的长度
    
    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, email={self.email})>"
