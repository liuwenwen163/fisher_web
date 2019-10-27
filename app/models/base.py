# encoding: utf-8
"""
初始化db
"""
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, SmallInteger

db = SQLAlchemy()


class Base(db.Model):
    __abstract__ = True  # 让base单纯作为基类，不要去创建数据表
    # create_time = Column('create_time', Integer)
    status = Column(SmallInteger, default=1)

    # 放到base模型的基类，其他继承这个base的都会有这个方法
    def set_attrs(self, attrs_dict):
        # 如果传入的字典里的某一个key，和模型里的属性是相同的，就将key对应的值赋给相关属性
        for key, value in attrs_dict.items():
            if hasattr(self, key) and key != 'id':
                setattr(self, key, value)