"""
    消息推送
    Message Push
    This module is licensed under GPL-3.0 License.
    @ OasisLee
    Date: 2022-05
"""

import requests
import json

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
    

    def bark(self, server="api.day.app", title="Bark", desp="test", autosave:bool=False, icon=None, group=None, level="active", url=None):
        # https://apps.apple.com/cn/app/bark-%E7%BB%99%E4%BD%A0%E7%9A%84%E6%89%8B%E6%9C%BA%E5%8F%91%E6%8E%A8%E9%80%81/id1403753865
        assert self.keys["bark"], "Bark key is not set"
        _paras = {
            "isArchive": autosave,
            "level": level

        }
        if group is not None: _paras["group"] = group
        if url is not None: _paras["url"] = url
        if icon is not None: _paras["icon"] = icon
        try:
            _req = requests.get("https://{}/{}/{}/{}".format(server, self.keys["bark"], title, desp), params=_paras, timeout=5)
        except Exception as e:
            print(e)
            return False
        if _dev: ic(_req.text, _req.status_code)
        if not _req.status_code == 200:
            print("Bark push failed. API response:{}".format(_req.text))
            return False
        else: return _req.text
    

    def qiye_weixin(self, title="test", type="text", desp="test", img=None):
        # https://developer.work.weixin.qq.com/document/path/91770
        assert self.keys["qiye_weixin"], "QiyeWeixin key is not set"
        if type in ("text", "markdown"):
            _data = {
                "msgtype": type,
                type: {
                    "content": desp
                }
            }
        elif type == "image":
            import base64
            import hashlib
            assert img, "Image object is required."
            assert base64.b64encode(img), "Image object is invalid."
            _data = {
                "msgtype": type,
                "image": {
                    "base64": base64.b64encode(img),
                    "md5": hashlib.md5(img).hexdigest()
                }
            }
        else: raise ValueError("Invalid message type.")
        _sendapi = requests.post("https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={}".format(self.keys["qiye_weixin"]), json=_data)
        if _dev: ic(_sendapi.text, _sendapi.status_code)
        if not _sendapi.status_code == 200:
            print("QiyeWeixin push failed. API returns a non-200 status code.[{}]".format(_sendapi.status_code))
            return False
        else:
            try:
                _resp = json.loads(_sendapi.text)
                if _resp["errcode"] == 0:
                    print("QiyeWeixin push success.")
                    return _resp
                else:
                    print("QiyeWeixin push failed. API returns a non-0 error code.[{}][{}]".format(_resp["errcode"], _resp["errmsg"]))
                    return False
            except:
                print("QiyeWeixin push failed. API returns a invalid response.")
                return False