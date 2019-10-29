# encoding: utf-8
from flask import Flask,request
from flask_login import LoginManager
from app.models.book import db

login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    # 指定装载哪个配置文件
    app.config.from_object('app.secure')
    app.config.from_object('app.setting')
    register_blueprint(app)
    # 将核心对象app和db数据库绑定
    db.init_app(app)
    # 初始化loginmanager
    login_manager.init_app(app)
    # 告诉login_manager登陆页面是哪个，以及登录提示信息
    login_manager.login_view = 'web.login'
    login_manager.login_message = '请先登录或注册'
    # 让sqlalchemy将所有数据模型映射到数据表
    db.create_all(app=app)
    return app


def register_blueprint(app):
    from app.web import web
    app.register_blueprint(web)
