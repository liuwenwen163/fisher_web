# encoding: utf-8
from fisher_classwork.httper import HTTP


class YuShuBook:
    isbn_url = "http://t.yushu.im/v2/book/isbn/{}"
    keyword_url = "http://t.yushu.im/v2/book/search?q={}&count={}&start={}"

    @classmethod
    def get_url_by_isbn(cls,isbn):
        url = cls.isbn_url.format(isbn)
        result = HTTP.get(url)
        return result

    @classmethod
    def get_url_by_name(cls,keyword,count=15,start=0):
        url = cls.keyword_url.format(keyword,count,start)
        result = HTTP.get(url)
        return result

