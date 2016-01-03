import json


def json_enc(obj):
    return obj.__dict__


def to_json(obj):
    return json.dumps(obj, default=json_enc, sort_keys=True)


def from_json(val):
    return json.loads(val)
