# encoding: utf-8
# 处理book的viewmodel，所以文件起名叫book


class BookViewModel:
    # 统一返回的数据结构，补齐缺少的数据
    @classmethod
    def package_single(cls, data, keyword):
        """
        处理返回的单本isbn的数据
        :param data: API返回的原始数据
        :param keyword: 查询的关键字
        :return: 返回给客户端的统一数据
        """
        returned = {
            'books': [],
            'total': 0,
            'keyword': keyword
        }
        if data:
            returned['total'] = 1
            returned['books'] = [cls.__cut_book_data(data)]
        return returned

    @classmethod
    def package_collection(cls, data, keyword):
        """
        处理keyword返回的集合数据，和处理 package_single 的返回数据是一样的
        :param data:API返回的原始数据
        :param keyword:
        :return:
        """
        returned = {
            'books': [],
            'total': 0,
            'keyword': keyword
        }
        if data:
            returned['total'] = data['total']
            # 使用列表生成式去复用单项数据的处理函数
            returned['books'] = [cls.__cut_book_data(book) for book in data['books']]
        return returned

    @classmethod
    def __cut_book_data(cls, data):
        """
        定义一个私有的处理原视数据的函数，处理原始数据，满足客户端显示的要求
        学习单个方法可以被两个业务所借鉴的方法
        :return:
        """

        book = {
            'title': data['title'],
            'publisher': data['publisher'],
            # page为空就会返回空字符串
            'pages': data['pages'] or '',
            'author': '、'.join(data['author']),
            'price': data['price'],
            'summary': data['summary'] or '',
            'image': data['image']
        }
        return book
