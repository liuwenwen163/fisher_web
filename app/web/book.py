# encoding: utf-8
from flask import jsonify, Blueprint

from helper import is_key_or_isbn
from yushu_book import YuShuBook

__author__ = "yc"

web = Blueprint('web', __name__)


@web.route('/book/search/<q>/<page>')
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
