# encoding: utf-8
import json
from flask import jsonify,request

from app.forms.book import SearchForm
from app.libs.helper import is_key_or_isbn
from app.spider.yushu_book import YuShuBook
from app.view_models.book import BookCollection
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
    books = BookCollection()

    if form.validate():
        q = form.q.data.strip()  # 去掉page前后的空格
        page = form.page.data
        key_or_isbn = is_key_or_isbn(q)
        yushu_book = YuShuBook()

        if key_or_isbn == "isbn":
            yushu_book.search_by_isbn(q)
        else:
            yushu_book.search_by_keyword(q, page)

        books.fill(yushu_book, q)
        return json.dumps(books, default=lambda o: o.__dict__)
    else:
        # flask的视图函数没有return语句是会报错的
        return jsonify(form.errors)

