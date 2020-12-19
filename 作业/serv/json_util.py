

from datetime import datetime, date
import json


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, (date, datetime)):
            return o.isoformat()        #Python对JSON中的特殊类型进行Encoder，Python 处理 JSON 数据时，dumps 函数是经常用到的。
                                        #原因在于 dumps 函数不知道如何处理 datetime 对象，默认情况下 json 模块使用 json.JSONEncoder 类来进行编码，此时我们需要自定义一下编码类。
        return json.JSONEncoder.default(self, o)


def json_dumps(obj):
    return json.dumps(obj, cls=JSONEncoder)


def json_loads(s):
    return json.loads(s)
