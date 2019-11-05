"""
所有用户操作的相关视图函数都在这个模块下面
"""
from flask import render_template, request, redirect, url_for, flash

from app import db
from app.forms.auth import RegisterForm, LoginForm, EmailForm
from app.models.user import User
from . import web
from flask_login import login_user, logout_user

__author__ = '七月'


@web.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        with db.auto_commit():
            user = User()
            user.set_attrs(form.data)
            db.session.add(user)
        return redirect(url_for('web.login'))
    return render_template('auth/register.html', form=form)


@web.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=True)
            next = request.args.get('next')
            # if not next or not next.startswith('/'):
            #     next = url_for('web.index')
            return redirect(next)
        else:
            flash('账号不存在或者密码错误')
    return render_template('auth/login.html',form=form)


@web.route('/reset/password', methods=['GET', 'POST'])
def forget_password_request():
    form = EmailForm(request.form)
    if request.method == 'POST':
        if form.validate():
            account_email = form.email.data
            # 如果没有查到用户名，first_or_404会抛出异常，后面的代码不会执行
            user = User.query.filter_by(email=account_email).first_or_404()
    return render_template('auth/forget_password_request.html', form=form)


@web.route('/reset/password/<token>', methods=['GET', 'POST'])
def forget_password(token):
    pass



@web.route('/change/password', methods=['GET', 'POST'])
def change_password():
    pass


@web.route('/logout')
def logout():
    # 使用flask_login提供的logout功能进行登出
    # 本质是清除了浏览器的cookie
    logout_user()
    return redirect(url_for('web.index'))
