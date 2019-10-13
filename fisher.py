# encoding: utf-8
from app import create_app

app = create_app()

# 调用run方法，启动web服务器
if __name__ == '__main__':
    print('启动app时候的内存地址：'+str(id(app)))
    app.run(host='0.0.0.0', debug=True)

