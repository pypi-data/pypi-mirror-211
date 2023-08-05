import json
from typing import Any


class JSONEncoderForClass(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        try:
            d = o.__dict__
        except TypeError:
            pass
        else:
            return d
        return json.JSONEncoder.default(self, o)


class MyJSONSer:
    @staticmethod
    def dumps(o: Any):
        return json.dumps(o, cls=JSONEncoderForClass)

    @staticmethod
    def dump(o: Any, fp):
        return json.dump(o, fp, cls=JSONEncoderForClass)

    @staticmethod
    def loads(s):
        return json.loads(s)

    @staticmethod
    def load(fp):
        return json.load(fp)
