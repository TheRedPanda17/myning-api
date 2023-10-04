from datetime import datetime


def jsonable(item: dict):
    transformed = {}
    for key, value in item.items():
        if isinstance(value, datetime):
            value = str(value)
        if isinstance(value, dict):
            value = jsonable(value)
        transformed[key] = value

    return transformed
