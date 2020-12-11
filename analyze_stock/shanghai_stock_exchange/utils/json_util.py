import json

class JsonEncoder(json.JSONEncoder):

    def default(self, o):

        if not isinstance(o, str):
            return str(o)

        super(JsonEncoder, self).default(o)
