# encoding: utf-8
"""
定义TradeInfo，转化从Gift表或者Wish表检索到的数据
使之符合页面的要求
"""

class TradeInfo:
    def __init__(self, goods):
        self.total = 0
        self.trades = []
        self.__parse(goods)

    def __parse(self, goods):
        """
        处理一组数据的转化
        :param goods:
        :return:
        """
        self.total = len(goods)
        self.trades = [self.__map_to_trade(single) for single in goods]

    def __map_to_trade(self, single):
        """
        处理单个的数据转换
        :param single:
        :return:
        """
        if single.create_datetime:
            time = single.create_datetime.strftime('%Y-%m-%d')
        else:
            time = '未知'
        return dict(
            user_name=single.user.nickname,
            time=time,
            id=single.id
        )


