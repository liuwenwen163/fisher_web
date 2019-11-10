# encoding: utf-8
from enum import Enum

class PendingStatus(Enum):
    """
        交易状态四种
    """
    Waiting = 1
    Success = 2
    Reject = 3
    Redraw = 4

    @classmethod
    def pending_str(cls, status, key):
        """
        类似switch-case语句，根据status和key的值返回不同的值
        外部调用status的时候，可以传入枚举的状态
        """
        key_map = {
            cls.Waiting: {
              'requester': '等待对方邮寄',
              'gifter': '等待你邮寄'
            },
            cls.Reject: {
                'requester': '对方已拒绝',
                'gifter': '你已拒绝'
            },
            cls.Redraw: {
                'requester': '你已撤销',
                'gifter': '对方已撤销'
            },
            cls.Success: {
                'requester': '对方已邮寄',
                'gifter': '你已邮寄，交易完成'
            },
        }
        return key_map[status][key]