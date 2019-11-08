# encoding: utf-8
from math import floor

from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash

from app import login_manager
from app.libs.enums import PendingStatus
from app.libs.helper import is_key_or_isbn
from app.models.base import Base, db
from sqlalchemy import Column, Integer, String, Boolean, Float
from flask_login import UserMixin

from app.models.drift import Drift
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
        """
        功能：验证用户的赠送此书，加入心愿清单传入数据是否有效
        第一步：验证isbn是否符合isbn规范
        第二步：验证根据isbn是否能查到书籍
        第三步：赠送或想要的这本书，不能已经存在于gift或者wish表中
        :param isbn: 书籍的isbn
        :return: True：标识isbn符合规范；False：表示isbn不符合规范
        """
        if is_key_or_isbn(isbn) != 'isbn':
            return False
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(isbn)
        if not yushu_book.first:
            return False
        gifting = Gift.query.filter_by(uid=self.id, isbn=isbn,
                                       launched=False).first()
        wishing = Wish.query.filter_by(uid=self.id, isbn=isbn,
                                       launched=False).first()
        if not gifting and not wishing:
            return True
        else:
            return False

    def generate_token(self, expiration=600):
        """
        对于token的要求：
        （1）记录用户的id号
        （2）必须是加密和编码的
        :param expiration: token的过期时间，单位秒
        :return:
        """
        from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'id': self.id}).decode('utf-8')

    @staticmethod
    def reset_password(token, new_password):
        """
        重置密码的视图函数
        :param token: 通过token拿到用户的id号
        :param new_password: 充值后的新密码
        :return:
        """
        from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        uid = data.get('id')
        with db.auto_commit():
            user = User.query.get(uid)
            user.password = new_password
        return True

    def can_send_drift(self):
        """
        1.鱼豆必须足够（大于等于1）
        2.每索取两本书，必须送出一本书：
        需要知道目前索取的书籍，和已经成功送出的书籍数量。
        :return:
        """
        # 判断鱼豆是否足够
        if self.beans < 1:
            return False

        # 查询成功赠送出的书籍
        success_gifts_count = Gift.query.filter_by(
            uid=self.id, launched=True
        ).count()
        # 查询成功接受了了多少书籍
        success_receive_count = Drift.query.filter_by(
            requester_id=self.id, pending=PendingStatus.Success
        ).count()
        return True if \
            floor(success_receive_count/2) <= floor(success_gifts_count) \
            else False

    @property
    def summary(self):
        return dict(
            nickname=self.nickname,
            beans=self.beans,
            email=self.email,
            send_recive=str(self.send_counter) + '/' + str(self.receive_counter)
        )




@login_manager.user_loader
def get_user(uid):
    return User.query.get(uid)
