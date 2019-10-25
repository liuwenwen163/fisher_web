# encoding: utf-8
"""
存放所有的视图函数
"""
from flask import Blueprint

web = Blueprint("web", __name__)

# 要在这里导入下注册的视图函数，否则相当于只定义了视图函数，没有引用
# 注意这里的导入要放到最后，否则还会发生循环导入
# 放到web前面，web还没实例化久导入book，book里又导入web，循环导入
from app.web import book
from app.web import auth
from app.web import drift
from app.web import gift
from app.web import main
from app.web import wish