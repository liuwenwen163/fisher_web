# encoding: utf-8
from flask import jsonify

from fisher import app
from helper import is_key_or_isbn
from yushu_book import YuShuBook

__author__ = "yc"

print('注册路由模块时的app地址：' + str(id(app)))
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
    return jsonify(result)
