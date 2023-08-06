"""
    消息推送
    Message Push
    This module is licensed under MIT License.
    @ OasisLee
    Date: 2022-05
"""

import requests

"""
    Development only
"""
_dev = False
if _dev:
    from icecream import ic

class MsgPush(object):

    def __init__(self, keytype, key):
        self.keys = {}
        self.keys[keytype] = key


    def serverchan(self, title="test", desp="test"):
        # https://sct.ftqq.com
        assert self.keys['serverchan'], "ServerChan key is not set"
        _data = {
            "title": title,
            "desp": desp
        }
        _sendapi = requests.post("https://sctapi.ftqq.com/{}.send".format(self.keys["serverchan"]), data=_data)
        if _dev: ic(_sendapi.text, _sendapi.status_code)
        if not _sendapi.status_code == 200:
            print("ServerChan push failed")
            return False
        else:
            print("ServerChan push success")
            return _sendapi.text