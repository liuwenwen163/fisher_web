# encoding: utf-8
"""
心愿清单的礼物模型
心愿书籍和对应想要的人名单
"""
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, func, desc
from sqlalchemy.orm import relationship

from app.models.base import Base, db
from app.spider.yushu_book import YuShuBook


class Wish(Base):
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
    def get_user_wishes(cls, uid):
        """
        返回用户的心愿
        :param uid:
        :return:
        """
        wishes = Wish.query.filter_by(
            uid=uid, launched=False).order_by(
            desc(Wish.create_time)).all()
        return wishes

    @classmethod
    def get_wishes_counts(cls, isbn_list):
        """
        计算心愿的数量
        :param isbn_list:检索到的isbn列表
        :return:
        """
        count_list = db.session.query(func.count(Gift.id), Gift.isbn).filter(
            Gift.launched == False,
            Gift.isbn.in_(isbn_list),
            Gift.status == 1).group_by(
            Gift.isbn).all()
        # 将返回的元组数据变为字典，外部人调用的时候就可以直接用key来访问了
        count_list = [{'count': w[0], 'isbn': w[1]} for w in count_list]
        return count_list


from app.models.gift import Gift