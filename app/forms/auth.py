# encoding: utf-8
"""
用户认证的表单处理数据
"""
from wtforms import Form, StringField, PasswordField
from wtforms.validators import Length, DataRequired, Email, ValidationError, EqualTo

from app.models.user import User


class RegisterForm(Form):
    email = StringField(validators=[DataRequired(), Length(8, 64),
                                    Email(message='电子邮箱不符合规范')])

    password = PasswordField(validators=[
        DataRequired(message='密码不可以为空，请输入你的密码'), Length(6, 32)])

    nickname = StringField(validators=[
        DataRequired(), Length(2, 10, message='昵称至少需要两个字符，最多10个字符')])

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('电子邮件已被注册')

    def validate_nickname(self, field):
        if User.query.filter_by(nickname=field.data).first():
            raise ValidationError('昵称已存在')



class LoginForm(Form):
    email = StringField(validators=[DataRequired(), Length(8, 64),
                                    Email(message='电子邮箱不符合规范')])

    password = PasswordField(validators=[
        DataRequired(message='密码不可以为空，请输入你的密码'), Length(6, 32)])


class EmailForm(Form):
    email = StringField(validators=[DataRequired(), Length(5, 64),
                                    Email(message='电子邮箱不符合规范')])


class ResetPasswordForm(Form):
    # 新密码
    password1 = PasswordField(validators=[
        DataRequired(),
        Length(6, 32, message='密码长度需要在6到20个字符之间'),
        EqualTo('password2', message='两次输入的密码不相同')
    ])
    # 确认密码
    password2 = PasswordField(validators=[
        DataRequired(),
        Length(6,32)
    ])