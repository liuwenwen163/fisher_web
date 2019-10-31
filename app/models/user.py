# encoding: utf-8
from werkzeug.security import generate_password_hash, check_password_hash

from app import login_manager
from app.libs.helper import is_key_or_isbn
from app.models.base import Base
from sqlalchemy import Column, Integer, String, Boolean, Float
from flask_login import UserMixin

from app.models.gift import Gift
from app.models.wish import Wish
from app.spider.yushu_book import YuShuBook


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

    def can_save_to_list(self, isbn):
        # 验证save_to_gift用户传入的isbn是否有效
        # 第一步：验证isbn是否符合isbn规范
        if is_key_or_isbn(isbn) != 'isbn':
            return False
        yushu_book = YuShuBook()
        # 第二步：验证根据isbn是否能查到书籍
        yushu_book.search_by_isbn(isbn)
        if not yushu_book.first:
            return False
        # 第三步：如果用户有一本书没有赠送出去，就不能再上传这本书了
        gifting = Gift.query.filter_by(uid=self.id, isbn=isbn,
                                       launched=False).first()
        # 第四步：一个用户不可能同时成为赠送者和索要者
        wishing = Wish.query.filter_by(uid=self.id, isbn=isbn,
                                       launched=False).first()
        # 合并三四步：图书必须要既不在赠送清单，也不在心愿清单才能添加
        if not gifting and not wishing:
            return True
        else:
            return False

@login_manager.user_loader
def get_user(uid):
    return User.query.get(uid)


