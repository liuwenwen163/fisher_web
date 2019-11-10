from flask import url_for, flash, render_template, request
from flask_login import login_required, current_user
from sqlalchemy import desc, or_
from werkzeug.utils import redirect

from app import db
from app.forms.book import DriftForm
from app.libs.email import send_mail
from app.libs.enums import PendingStatus
from app.models.drift import Drift
from app.models.gift import Gift
from app.models.user import User
from app.view_models.book import BookViewModel
from app.view_models.drift import DriftCollection
from . import web

__author__ = '七月'


@web.route('/drift/<int:gid>', methods=['GET', 'POST'])
@login_required
def send_drift(gid):
    """
    首先要进行条件检测，是否满足能够交易的条件：
    1.自己不能够向自己请求书籍
    2.鱼豆必须足够
    3.每索取两本书，必须要送出一本书
    :param gid:
    :return:
    """
    current_gift = Gift.query.get_or_404(gid)
    # 判断是否是用户自己的书
    if current_gift.is_yourself_gift(current_user.id):
        flash('这本书是你自己的，不能向自己索要书籍')
        return redirect(url_for('web.book_detail', isbn=current_gift.isbn))

    # 检测是否满足赠送图书的后两个条件
    can = current_user.can_send_drift()
    if not can:
        return render_template('not_enough_beans.html', beans=current_user)

    form = DriftForm(request.form)
    if request.method == 'POST' and form.validate():
        save_drift(form, current_gift)
        # 发送一封邮件提醒有人想索要书籍
        send_mail(
            current_gift.user.email,
            '有人想要一本书', 'email/get_gift.html',
            wisher=current_user, gift=current_gift
        )
        return redirect(url_for('web.pending'))

    gifter = current_gift.user.summary
    return render_template('drift.html', gifter=gifter,
                           user_beans=current_user.beans, form=form)


@web.route('/pending')
@login_required
def pending():
    """
    requester_id和gifter_id之间是或关系，
    筛选出来的记录才是作为赠送者或者是请求人.
    方法：使用filter结合or_，or括号里面的条件就是或关系
    :return:
    """
    drifts = Drift.query.filter(
        or_(Drift.requester_id==current_user.id,
        Drift.gifter_id==current_user.id)
    ).order_by(desc(Drift.create_time)).all()

    views = DriftCollection(drifts, current_user.id)
    return render_template('pending.html', drifts=views.data)


@web.route('/drift/<int:did>/reject')
@login_required
def reject_drift(did):
    with db.auto_commit():
        drift = Drift.query.filter(
            Gift.uid == current_user.id,
            Drift.id == did
        ).first_or_404()
        drift.pending = PendingStatus.Reject
        requester = User.query.get_or_404(drift.requester_id)
        requester.beans += 1
    return redirect(url_for('web.pending'))


@web.route('/drift/<int:did>/redraw')
@login_required
def redraw_drift(did):
    """
    撤销drift
    :param did: drift 的 id 号
    :return:
    """
    with db.auto_commit():
        drift = Drift.query.filter_by(
            requester_id=current_user.id, id=did).first_or_404()
        drift.pending = PendingStatus.Redraw
        current_user.beans += 1
    return redirect(url_for('web.pending'))


@web.route('/drift/<int:did>/mailed')
def mailed_drift(did):
    pass

def save_drift(drift_form, current_gift):
    with db.auto_commit():
        drift = Drift()
        # 使用poplutate_obj，如果模型中字段的名称和form中字段名称相同
        # 就可以将form中的模型字段拷贝到drift模型中
        drift_form.populate_obj(drift)

        drift.gift_id = current_gift.id
        drift.requester_id = current_user.id
        drift.requester_nickname = current_user.nickname
        drift.gifter_nickname = current_gift.user.nickname
        drift.gifter_id = current_gift.user.id

        # book原本是字典，需要通过字典的方式来访问
        # 为了保证调用的统一性将current_gift获取到的数据
        # 用BookViewModel构建成一个对象
        book = BookViewModel(current_gift.book)

        drift.book_title = book.title
        drift.book_author = book.author
        drift.book_img = book.image
        drift.isbn = book.isbn

        current_user.beans -= 1

        db.session.add(drift)