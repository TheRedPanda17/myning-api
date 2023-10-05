from datetime import datetime


def jsonable(item: dict | list):
    if isinstance(item, list):
        return [jsonable(v) for v in item]

    transformed = {}
    for key, value in item.items():
        if isinstance(value, datetime):
            value = str(value)
        if isinstance(value, dict):
            value = jsonable(value)
        transformed[key] = value

    return transformed
