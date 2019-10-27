# encoding: utf-8
from app import db
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship


class Gift(db.Model):
    id = Column(Integer, primary_key=True)
    user = relationship('User')  # 和模型User建立关系
    uid = Column(Integer, ForeignKey('user.id'))  # uid是user模型下的id号
    # 本地没有存储书籍信息，所以不能用这种方法，可以用isbn编号来表示关系
    # book = relationship('Book')
    # bid = Column(Integer, ForeignKey('book.id'))
    isbn = Column(String(15), nullable=False)
    launched = Column(Boolean, default=False)  # 表示礼物是否赠送出去
