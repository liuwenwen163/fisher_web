# encoding: utf-8
import json

from flask import Flask, make_response, jsonify

from fisher_classwork.helper import is_key_or_isbn
from fisher_classwork.yushu_book import YuShuBook

__author__ = "yc"

# 传入参数作为app的核心标识
app = Flask(__name__)


@app.route('/book/search/<q>/<page>')
def search(q,page):
    """
    q: 普通关键字 或 isbn
    page
    """
    key_or_isbn = is_key_or_isbn(q)
    if key_or_isbn == "isbn":
        result = YuShuBook.get_url_by_isbn(q)
    else:
        result = YuShuBook.get_url_by_name(q)
        # json.dumps 序列化 dict
        # 使用 flask 自带的jsonify来替代下面一长串代码
    return jsonify(result)
    # return json.dumps(result), 200, {'content-type':'application/json'}



# 调用run方法，启动web服务器
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
