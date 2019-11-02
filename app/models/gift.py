# encoding: utf-8
"""
赠送书籍的礼物模型
管理要赠送的书籍和赠书人的清单列表
"""
from flask import current_app
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, desc
from sqlalchemy.orm import relationship

from app.models.base import Base
from app.spider.yushu_book import YuShuBook


class Gift(Base):
    id = Column(Integer, primary_key=True)
    user = relationship('User')  # 和模型User建立关系
    uid = Column(Integer, ForeignKey('user.id'))  # uid是user模型下的id号
    # 本地没有存储书籍信息，所以不能用这种方法，可以用isbn编号来表示关系
    # book = relationship('Book')
    # bid = Column(Integer, ForeignKey('book.id'))
    isbn = Column(String(15), nullable=False)
    launched = Column(Boolean, default=False)  # 表示礼物是否赠送出去

    @property
    def book(self):
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(self.isbn)
        return yushu_book.first

    @classmethod
    def recent(cls):
        """
        先根据isbn进行分组（分组后才能去重），然后按照时间进行排序
        限制显示数量为30本
        然后用distinct()进行去重（需要先分组才能去重）
        :return:
        """
        recent_gift = Gift.query.filter_by(
            launched=False).group_by(
            Gift.isbn).order_by(
            desc(Gift.create_time)).limit(
            current_app.config['RECENT_BOOK_COUNT']).distinct().all()
        return recent_gift
