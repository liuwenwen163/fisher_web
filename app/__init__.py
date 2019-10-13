# encoding: utf-8
from flask import Flask


def create_app():
    app = Flask(__name__)
    print('初始化app时候的内存地址：' + str(id(app)))
    app.config.from_object('config')
    return app