# encoding: utf-8
from flask import Flask

__author__ = "yc"

app = Flask(__name__)
app.config.from_object('config')

# 调用run方法，启动web服务器
if __name__ == '__main__':
    print(id(app))
    app.run(host='0.0.0.0', debug=True)
