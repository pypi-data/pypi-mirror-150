import json


def bypass(data):
    return data


def to_caped_str(data, limit=30):
    result = str(data)

    if len(result) > limit:
        return result[: 30]

    return data


def to_json(data):
    return json.dumps(data)
