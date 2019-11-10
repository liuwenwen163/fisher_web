# encoding: utf-8
"""
初始化db
"""
from datetime import datetime
from contextlib import contextmanager

from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy, BaseQuery
from sqlalchemy import Column, Integer, SmallInteger



class SQLAlchemy(_SQLAlchemy):
    """
    将原来的SQLAlchemy导入时改个名字，继承它
    继承的基础上添加方法，简化try-except语句的书写重复度
    """
    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e


class Query(BaseQuery):
    def filter_by(self, **kwargs):
        """
        对query.filter_by自己添加一个status状态，
        status=1表示只检索没有软删除的商品
        :param kwargs:
        :return:
        """
        # 实现自己添加的逻辑
        if 'status' not in kwargs.keys():
            kwargs['status'] = 1
        # 完成原有的filter_by逻辑
        return super(Query, self).filter_by(**kwargs)


db = SQLAlchemy(query_class=Query)  # 用自定义的Query替换原有的Query


class Base(db.Model):
    __abstract__ = True  # 让base单纯作为基类，不要去创建数据表
    create_time = Column('create_time', Integer)
    status = Column(SmallInteger, default=1)

    def __init__(self):
        self.create_time = int(datetime.now().timestamp())

    # 放到base模型的基类，其他继承这个base的都会有这个方法
    def set_attrs(self, attrs_dict):
        # 如果传入的字典里的某一个key，和模型里的属性是相同的，就将key对应的值赋给相关属性
        for key, value in attrs_dict.items():
            if hasattr(self, key) and key != 'id':
                setattr(self, key, value)

    @property
    def create_datetime(self):
        if self.create_time:
            return datetime.fromtimestamp(self.create_time)
        else:
            return None

    def delete(self):
        self.status = 0