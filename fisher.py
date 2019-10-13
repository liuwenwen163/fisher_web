# encoding: utf-8
from flask import Flask

__author__ = "yc"

app = Flask(__name__)
print('初始化app时候的内存地址：'+str(id(app)))
app.config.from_object('config')

from app.web import book

# 调用run方法，启动web服务器
if __name__ == '__main__':
    print('启动app时候的内存地址：'+str(id(app)))
    app.run(host='0.0.0.0', debug=True)
