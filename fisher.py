# encoding: utf-8
from app import create_app

app = create_app()

# 调用run方法，启动web服务器
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=app.config['DEBUG'], threaded=True, processes = 1)


