# encoding: utf-8
from sqlalchemy import Column, Integer, String, SmallInteger

from app.libs.enums import PendingStatus
from app.models.base import Base


class Drift(Base):
    """
        保存一次具体的交易信息
    """
    id = Column(Integer, primary_key=True)

    # 邮寄信息
    recipient_name = Column(String(20), nullable=False)
    address = Column(String(100), nullable=False)
    message = Column(String(200))
    mobile = Column(String(20), nullable=False)

    # 书籍信息
    isbn = Column(String(13))
    book_title = Column(String(50))
    book_author = Column(String(30))
    book_img = Column(String(50))

    # 请求者信息
    requester_id = Column(Integer)
    requester_nickname = Column(String(20))

    # 赠送者信息
    gifter_id = Column(Integer)
    gift_id = Column(Integer)
    gifter_nickname = Column(String(20))

    # 表示鱼漂（交易）的状态
    _pending = Column('pending', SmallInteger, default=1)

    @property
    def pending(self):
        """
        读取数字类型的_pending，将其转化为枚举类型返回
        这样读取的时候返回的就是可读的枚举
        :return: 返回枚举类型的数据
        """
        return PendingStatus(self._pending)

    @pending.setter
    def pending(self, status):
        """
        将枚举类型转换成数字类型
        当我们设置pending时，实际上传入的是枚举类型，通过调用 status.value
        返回实际的数字类型存入数据库
        :param status:
        :return: 返回数字类型的状态
        """
        self._pending = status.value
