# encoding: utf-8

from flask import Flask, current_app
app = Flask(__name__)


# # 获取 flask 的 AppContext
# ctx = app.app_context()
# ctx.push() # 入栈
# a = current_app
# d = current_app.config['DEBUG']
# ctx.pop() # 手动出栈

# 5-4 使用with语句改写
# app_context() : 上下文管理器
# app.app_context() : 上下文表达式
# with app.app_context():
#     a = current_app
#     b = current_app.config['DEBUG']


# # 使用as语法,打开为某一对象,在内部可以使用
# with open(r'D:\a.txt') as f:
#     print(f.read())
#
#
# 5-5 __exit__ 方法
class MyResource:
    # MyResource 是上下文管理器
    def __enter__(self):
        print('connect to resource')
        # 将 MyResource 类的对象返回回去
        # self是上下文管理器本身
        return self

    def __exit__(self, exc_type, exc_value, tb):
        # __eixt__ 作用:回收资源,处理异常
        # exit 方法保证了即使发生异常,也能执行方法内部的代码,对资源进行回收
        # 多出来三个参数,是用来处理异常的,没有异常,三个参数就是空值
        if tb:
            print('Process exception!')
        else:
            print('No exception.')
        print('close resource connection')
        # exit也要有返回值,只有两种返回值:true或false,没有return代表返回了fasle
        # False:exit执行完之后,在with语句外部还会抛出异常,比如外面有try-except
        # True:with语句内部已经处理了异常,python在with外部不要再抛出异常了
        return False

    # 定义一个业务方法
    def query(self):
        print('query data')

# # 正常流程
# with MyResource() as resource:
#     resource.query()

# # 报错的流程
# with MyResource() as resource:
#     1/0  # 抛出异常
#     resource.query()

# try except 捕捉错误
try:
    with MyResource() as resource:
        1/0  # 抛出异常
        resource.query()
except Exception as e:
    print(e)