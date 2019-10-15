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

