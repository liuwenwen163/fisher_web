# encoding: utf-8
import json
from flask import jsonify, request, flash, render_template
from flask_login import current_user

from app.forms.book import SearchForm
from app.libs.helper import is_key_or_isbn
from app.models.gift import Gift
from app.models.wish import Wish
from app.spider.yushu_book import YuShuBook
from app.view_models.book import BookCollection, BookViewModel
from app.view_models.trade import TradeInfo

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
    else:
        flash('搜索的关键字不符合要求，请重新输入关键字。')
    # return 放到外面确保视图函数总有返回结果
    return render_template('search_result.html', books=books, form=form)


@web.route('/book/<isbn>/detail')
def book_detail(isbn):
    """
    使用has_in_gifts和has_in_wishes描述三种状态：
    ①书既不在该用户的礼物清单也不在心愿清单
    ②书在礼物清单，不在心愿清单
    ③书在心愿清单，不在礼物清单
    用户没有登陆，按照既不在赠送清单也不在心愿清单来处理；
    用户有登录，去Gift和Wish表里做查找，能查找到的话，就说明在对应的清单中
    :param isbn:
    :return:
    """
    has_in_gifts = False
    has_in_wishes = False
    # 判断wish或者gift表格中，是否有wish或gift记录，二者互斥
    if current_user.is_authenticated:
        if Gift.query.filter_by(uid=current_user.id, isbn=isbn, launched=False).all():
            has_in_gifts = True
        if Wish.query.filter_by(uid=current_user.id, isbn=isbn, launched=False).all():
            has_in_wishes = True

    # 获取书籍详情数据
    yushu_book = YuShuBook()
    yushu_book.search_by_isbn(isbn)
    book = BookViewModel(yushu_book.first)

    # 获取全部想要书籍人的清单和赠送人的清单
    trade_gifts = Gift.query.filter_by(isbn=isbn, launched=False).all()
    trade_wishes = Wish.query.filter_by(isbn=isbn, launched=False).all()

    # 调用viewModel转化请求到的数据
    trade_gifts_model = TradeInfo(trade_gifts)
    trade_wishes_model = TradeInfo(trade_wishes)

    return render_template('book_detail.html',
                           book=book,
                           wishes=trade_wishes_model, gifts=trade_gifts_model,
                           has_in_gifts=has_in_gifts,
                           has_in_wishes=has_in_wishes)
