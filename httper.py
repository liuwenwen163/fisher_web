# encoding: utf-8
import requests

class HTTP:
    @staticmethod
    def get(url, return_json=True):
        # 传入了一个self，但是没有用，是静态方法
        r = requests.get(url)
        if r.status_code != 200:
            return {} if return_json else ''
        return r.json() if return_json else r.text
        # # 不简便的写法
        # if r.status_code == 200:
        #     if return_json:
        #         return r.json()
        #     else:
        #         return r.text
        # else:
        #     if return_json:
        #         return {}
        #     else:
        #         return ""
