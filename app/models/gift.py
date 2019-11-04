# encoding: utf-8
"""
赠送书籍的礼物模型
管理要赠送的书籍和赠书人的清单列表
"""
from flask import current_app
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, desc, func
from sqlalchemy.orm import relationship

from app.models.base import Base, db
from app.models.wish import Wish
from app.spider.yushu_book import YuShuBook


class Gift(Base):
    """
    模型Gift可以理解为数据库中的一条记录
    """
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

    # 对象代表一个礼物
    # 类代表礼物这个事物，它是抽象，不是具体的‘一个’
    @classmethod
    def recent(cls):
        """
        最近的礼物，属于某一类事务，所以用类方法
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

    @classmethod
    def get_user_gifts(cls, uid):
        gifts = Gift.query.filter_by(
            uid=uid, launched=False).order_by(desc(
            Gift.create_time)).all()
        return gifts

    @classmethod
    def get_wish_counts(cls, isbn_list):
        """
        根据传入的一组isbn列表，到Wish表中计算出某个礼物，
        的wish心愿数量
        查询数量，使用query就不太方便了
        由于需要查询一组数量，因此要用group_by
        :param isbn_list:检索到的isbn列表
        :return:
        """
        count_list = db.session.query(func.count(Wish.id), Wish.isbn).filter(
            Wish.launched == False,
            Wish.isbn.in_(isbn_list),
            Wish.status == 1).group_by(
            Wish.isbn).all()
        # 将返回的元组数据变为字典，外部人调用的时候就可以直接用key来访问了
        count_list = [{'count': w[0], 'isbn': w[1]} for w in count_list]
        return count_list