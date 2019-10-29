# encoding: utf-8
from werkzeug.security import generate_password_hash, check_password_hash

from app import login_manager
from app.models.base import Base
from sqlalchemy import Column, Integer, String, Boolean, Float
from flask_login import UserMixin


# 创建User的数据模型
class User(UserMixin, Base):
    id = Column(Integer, primary_key=True)
    nickname = Column(String(24), nullable=False)
    phone_number = Column(String(18), unique=True)
    # 如果不希望数据库表字段等于左边的名称就需要进行修改了
    _password = Column('password', String(128), nullable=False)
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

    def check_password(self, raw):
        # 验证用户密码,第一个参数是加密的密码，第二个参数是用户输入的明文密码。返回T/F。
        return check_password_hash(self._password, raw)

    def get_id(self):
        return self.id

@login_manager.user_loader
def get_user(uid):
    return User.query.get(uid)