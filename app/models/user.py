# encoding: utf-8
from werkzeug.security import generate_password_hash

from app.models.base import Base
from sqlalchemy import Column, Integer, String, Boolean, Float


# 创建User的数据模型
class User(Base):
    id = Column(Integer, primary_key=True)
    nickname = Column(String(24), nullable=False)
    phone_number = Column(String(18), unique=True)
    # 如果不希望数据库表字段等于左边的名称就需要进行修改了
    _password = Column('password', String(128))
    email = Column(String(50), unique=True, nullable=False)
    confirmed = Column(Boolean, default=False)
    beans = Column(Float, default=0)
    send_counter = Column(Integer, default=0)
    receive_counter = Column(Integer, default=0)
    wx_open_id = Column(String(50))
    wx_name = Column(String(32))

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        # 对原始密码加密，加密之后再赋给_password
        self._password = generate_password_hash(raw)


