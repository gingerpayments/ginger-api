import json
import decimal
import datetime


class GingerJSONEncoder(json.JSONEncoder):
    """
    Custom JSON encoder with additional support
    """
    def default(self, object):
        if isinstance(object, decimal.Decimal):
            return str(object)

        if isinstance(object, set):
            return list(object)

        if isinstance(object, datetime.datetime):
            return object.isoformat()

        return json.JSONEncoder.default(self, object)
