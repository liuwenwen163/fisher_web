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

#
# # 6-13 小节线程隔离对象的测试代码，可删
# @web.route('/test')
# def test1():
#     from flask import request
#     from test_tmp.tmp_none_local import n
#     print(n.v)
#     n.v = 2
#     print(n.v)
#     print('--------------------')
#     print(getattr(request, 'v', 'None Value'))
#     print(setattr(request, 'v', 100))
#     print(getattr(request, 'v'))
#     return ''

# 6-14 验证current_app是否全局只有一个，可删
@web.route('/test')
def test1():
    from flask import current_app,request
    print(str(id(current_app)) + ',' + str(id(request)))
    return ''
