# encoding: utf-8
"""
处理book的viewmodel，加工原视数据，并返回统一格式的数据
"""

# 重构是颠覆性的，所以不在原来基础上改了
class BookViewModel:
    # 最终用来处理单本书籍的数据
    def __init__(self, book):
        self.title = book['title']
        self.publisher = book['publisher']
        self.author = '、'.join(book['author'])
        self.image = book['image']
        self.price = book['price']
        self.summary = book['summary']
        self.isbn = book['isbn']
        self.pages = book['pages']
        self.pubdate = book['pubdate']
        self.binding = book['binding']

    @property
    def intro(self):
        intros = filter(lambda x: True if x else False,
                        [self.author, self.publisher, self.price])
        return '/'.join(intros)


class BookCollection:
    # 这个类是一个集合
    def __init__(self):
        self.total = 0
        self.books = []
        self.keyword = ''

    def fill(self, yushu_book, keyword):
        # 接收yushu_book(原始书籍数据)
        self.total = yushu_book.total
        self.keyword = keyword
        self.books = [BookViewModel(book) for book in yushu_book.books]

