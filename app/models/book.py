# encoding: utf-8
"""
存放book，书籍这个模型
"""
from sqlalchemy import Column, Integer, String
from app.models.base import db, Base


# 使用 Flask_SQLAlchemy 操作数据库
class Book(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50), nullable=False)
    author = Column(String(30), default='未名')
    binding = Column(String(20))  # 精装/平装
    publisher = Column(String(50)) # 出版社
    price = Column(String(20))
    pages = Column(Integer)
    pubdate = Column(String(20))  # 出版年月
    isbn = Column(String(15), nullable=False, unique=True) # 索引不需要重复
    summary = Column(String(1000))  # 书籍简介
    image = Column(String(50))  # 存放书籍图片

