# encoding: utf-8
from .book import BookViewModel


class MyWishes:
    def __init__(self, wishes_of_mine, gift_count_list):
        self.wishes = []

        self.__wishes_of_mine = wishes_of_mine
        self.__gift_count_list = gift_count_list

        self.wishes = self.__parse()

    def __parse(self):
        temp_wishes = []
        for wish in self.__wishes_of_mine:
            my_wish = self.__matching(wish)
            temp_wishes.append(my_wish)
        return temp_wishes

    def __matching(self, gift):
        count = 0
        for wish_count in self.__gift_count_list:
            if gift.isbn == wish_count['isbn']:
                count = wish_count['count']
        # 为了方便后面进行REST API序列化，所以返回字典
        r = {
            'wishes_count': count,
            'book': BookViewModel(gift.book),
            'id': gift.id
        }
        return r
