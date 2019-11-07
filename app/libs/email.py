# encoding: utf-8
from threading import Thread

from flask import current_app, render_template

from app import mail
from flask_mail import Message


def send_sync_email(app, msg):
    with app.app_context():
        try:
            mail.send(msg)
        except Exception as e:
            print(e)


def send_mail(to, subject, template, **kwargs):
    """
    定义发送邮件功能的函数，实现向用户发送邮件
    Message需要传入的参数：邮件主题，发件人，收件人，主体内容
    :param to:邮件发给谁
    :param subject:邮件主题
    :param template:邮件模板
    :return:
    """
    msg = Message('[鱼书]' + ' ' + subject,
                  sender=current_app.config['MAIL_USERNAME'],
                  recipients=[to])
    msg.html = render_template(template, **kwargs)
    app = current_app._get_current_object()
    # 通过args向异步的函数传递参数
    thr = Thread(target=send_sync_email, args=[app,msg])
    thr.start()
