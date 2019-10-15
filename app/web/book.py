# encoding: utf-8
from flask import jsonify,request

from app.forms.book import SearchForm
from app.libs.helper import is_key_or_isbn
from app.spider.yushu_book import YuShuBook
from . import web

__author__ = "yc"


# @web.route('/book/search/<q>/<page>')
@web.route('/book/search')
def search():
    """
        q: 普通关键字 或 isbn
        page
        """
    form = SearchForm(request.args)
    if form.validate():
        q = form.q.data.strip()  # 去掉page前后的空格
        page = form.page.data
        key_or_isbn = is_key_or_isbn(q)
        if key_or_isbn == "isbn":
            result = YuShuBook.get_url_by_isbn(q)
        else:
            result = YuShuBook.get_url_by_name(q, page)
        return jsonify(result)
    else:
        # flask的视图函数没有return语句是会报错的
        return jsonify(form.errors)