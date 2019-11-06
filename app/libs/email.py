# encoding: utf-8
from flask import current_app, render_template

from app import mail
from flask_mail import Message


def send_mail(to, subject, template, **kwargs):
    """
    定义发送邮件功能的函数，实现向用户发送邮件
    :param to:邮件发给谁
    :param subject:邮件主题
    :param template:邮件模板
    :return:
    """
    # msg = Message('测试邮件',
    #               sender='1227259056@qq.com',
    #               body='Test',
    #               recipients=['bowen513s@163.com'])
    msg = Message('[鱼书]' + ' ' + subject,
                  sender=current_app.config['MAIL_USERNAME'],
                  recipients=[to])
    msg.html = render_template(template, **kwargs)
    mail.send(msg)
