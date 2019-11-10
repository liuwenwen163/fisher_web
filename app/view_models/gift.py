# encoding: utf-8
from .book import BookViewModel
# from collections import namedtuple

# 为了方便序列化，就不使用namedtuple
# 如果用namedtuple来实现MyGift就是下面的方法：
# MyGift = namedtuple('MyGift', ['id', 'book', 'wishes_count'])


class MyGifts:
    def __init__(self, gifts_of_mine, wish_count_list):
        """

        :param gifts_of_mine: Gift表中根据用户id号检索出的原始数据
        :param wish_count_list: 每一种礼物对应的心愿数量
        """
        self.gifts = []

        self.__gifts_of_mine = gifts_of_mine
        self.__wish_count_list = wish_count_list

        self.gifts = self.__parse()

    def __parse(self):
        temp_gifts = []
        for gift in self.__gifts_of_mine:
            my_gift = self.__matching(gift)
            temp_gifts.append(my_gift)
        return temp_gifts

    def __matching(self, gift):
        count = 0
        for wish_count in self.__wish_count_list:
            if gift.isbn == wish_count['isbn']:
                count = wish_count['count']
        # 为了方便后面进行REST API序列化，所以返回字典
        r = {
            'wishes_count': count,
            'book': BookViewModel(gift.book),
            'id': gift.id
        }
        return r
        # 这里注销掉的代码，使用了上面的namedtuple
        # my_gift = MyGift(gift.id, BookViewModel(gift.book), count)
        # return my_gift

