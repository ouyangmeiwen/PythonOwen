from sqlalchemy import Column, Integer, String, Unicode, Sequence
from sqlalchemy.ext.declarative import declarative_base
from base.basemodel import Base

# 定义 Oracle 用的 User 模型
class User_Oracle(Base):
    __tablename__ = 'users'

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    username = Column(Unicode(100), unique=False)
    email = Column(String(255), unique=False)

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, email={self.email})>"
