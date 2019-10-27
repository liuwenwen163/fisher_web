# encoding: utf-8
"""
YuShuBook 负责查询并存储书籍的数据
"""
from app.libs.httper import HTTP
from flask import current_app


class YuShuBook:
    isbn_url = "http://t.yushu.im/v2/book/isbn/{}"
    keyword_url = "http://t.yushu.im/v2/book/search?q={}&count={}&start={}"

    def __init__(self):
        # 保存对象的数据
        # 将keyword和isbn两种不同返回的数据进行统一
        self.total = 0
        self.books = []

    def search_by_isbn(self, isbn):
        url = self.isbn_url.format(isbn)
        result = HTTP.get(url)
        self.__fill_single(result)

    def search_by_keyword(self, keyword, page=1):
        url = self.keyword_url.format(keyword, current_app.config['PER_PAGE'], self.calculate_start(page))
        result = HTTP.get(url)
        self.__fill_collection(result)

    def __fill_single(self, data):
        if data:
            self.total = 1
            self.books.append(data)

    def __fill_collection(self, data):
        self.total = data['total']
        self.books = data['books']

    def calculate_start(self, page):
        return (page-1)*current_app.config['PER_PAGE']

    # 内部封装，良好接口调用，外面可以像调用属性一样获取正确的数据
    @property
    def first(self):
        return self.books[0] if self.total >=1 else None
