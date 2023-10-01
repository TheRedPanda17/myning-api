import base64

from aiohttp import web

from story import database


async def create_user(request: web.Request):
    content: dict = await request.json()
    errors = []

    name = content.get("name")
    if not name:
        errors.append("'name' must not be empty")
    else:
        exists = await database.users.get_user_by_name(name)
        if exists:
            errors.append(f"The name '{name}' is already taken")

    password = content.get("password")
    if not password:
        errors.append("'password' must not be empty")

    if errors:
        return web.json_response(data={"errors": errors}, status=400)

    result = await database.users.create_user(name=name, password=password)
    if not result:
        return web.json_response(status=500)

    result["created_dt"] = str(result["created_dt"])
    result["updated_dt"] = str(result["updated_dt"])

    return web.json_response(data=result, status=200)


async def update_user(request: web.Request):
    _id = request.path_qs.split("/")[-1]
    if _id.isdigit():
        _id = int(_id)
    else:
        return web.json_response(data={"erros": ["'id' must be an integer"]})

    user = await database.users.get_user(_id)
    if not user:
        return web.json_response(status=404)

    content: dict = await request.json()
    errors = []

    name = content.get("name")
    if not name:
        errors.append("'name' must not be empty")
    else:
        exists = await database.users.get_user_by_name(name)
        if exists:
            errors.append(f"The name '{name}' is already taken")

    password = content.get("password")
    if not password:
        errors.append("'password' must not be empty")

    if errors:
        return web.json_response(data={"errors": errors}, status=400)

    result = await database.users.update_user(_id=_id, name=name, password=password)
    if not result:
        return web.json_response(status=500)

    print("RESULT")
    print(result)
    result["created_dt"] = str(result["created_dt"])
    result["updated_dt"] = str(result["updated_dt"])

    return web.json_response(data=result, status=200)


async def get_users(_: web.Request):
    users = await database.users.get_users()
    for user in users:
        user["created_dt"] = str(user["created_dt"])
        user["updated_dt"] = str(user["updated_dt"])

    return web.json_response(data=users, status=200)
