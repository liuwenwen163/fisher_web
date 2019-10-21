# encoding: utf-8

# # 6-3 多线程
import threading,time
#
# def worker():
#     print('I am thresd.')
#     t = threading.current_thread()
#     time.sleep(5)
#     print(t.getName())
#
# # 定义线程
# new_t = threading.Thread(target=worker)
# # 启动线程
# new_t.start()
#
# # print('I am yc.')
# t = threading.current_thread()
# print(t.getName())

# # 6-9 Flask 中的线程隔离对象Local
# from werkzeug.local import Local
#
# my_obj = Local()
# my_obj.b = 1
#
# def worker():
#     # 新线程中去修改Local对象的变量
#     my_obj.b = 2
#     print('In new thred b is :' + str(my_obj.b))
#
# new_t = threading.Thread(target=worker, name='yc_thread')
# new_t.start()
# time.sleep(1)
# # 查看主线程中变量是否有改变
# print('In main thread b is :' + str(my_obj.b))

#
# # 6-11 LocalStack 的基本用法
# from werkzeug.local import LocalStack
#
# s = LocalStack()
# s.push(1)
# print(s.top)  # 取栈顶的元素
# print(s.top)  # 取栈顶的元素
# print(s.pop())  # 栈顶元素弹出
# # 栈顶元素被弹出了，所以栈顶元素为空
# print(s.top)
#
# s.push(1)
# s.push(2)
# print(s.top)
# print(s.top)
# print(s.pop())
# print(s.top)



# 6-12 LocalStack作为线程隔离对象的意义
from werkzeug.local import LocalStack

my_stack = LocalStack()
my_stack.push(1)
print('In main thread after push, value is:' + str(my_stack.top))

def worker():
    # 新线程是取不到主线程推入的元素，所以此处打印为空
    print('In new thread before push,value is :' + str(my_stack.top))
    my_stack.push(2)
    print('In new thread after push,value is :' + str(my_stack.top))


new_t = threading.Thread(target=worker, name='yc_thread')
new_t.start()
time.sleep(1)
# 查看主线程中变量是否有改变
print('In main thread b is :' + str(my_stack.top))






