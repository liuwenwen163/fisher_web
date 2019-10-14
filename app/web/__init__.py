# encoding: utf-8
from flask import Blueprint

web = Blueprint("web", __name__)

# 要在这里导入下注册的视图函数，否则相当于只定义了视图函数，没有引用
# 注意这里的导入要放到最后，否则还会发生循环导入
# 放到web前面，web还没实例化久导入book，book里又导入web，循环导入
from .book import search
