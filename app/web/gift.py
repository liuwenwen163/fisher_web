from flask_login import login_required,current_user

from app import db
from app.models.gift import Gift
from . import web
__author__ = '七月'


@web.route('/my/gifts')
@login_required
def my_gifts():
    return 'my gifts'


@web.route('/gifts/book/<isbn>')
@login_required
def save_to_gifts(isbn):
    # 赠送此书功能的视图函数
    gift = Gift()
    gift.isbn = isbn
    gift.uid = current_user.id
    current_user.beans += current_user.config['BEANS_UPLOAD_ONE_BOOK ']
    db.session.add(gift)
    db.session.commit()


@web.route('/gifts/<gid>/redraw')
def redraw_from_gifts(gid):
    pass



