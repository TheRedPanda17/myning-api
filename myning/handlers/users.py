from aiohttp import web

from myning import database
from myning.utils.auth import authed
from myning.utils.errors import wrap_errors
from myning.utils.transforming import jsonable


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
        return wrap_errors(errors)

    result = await database.users.create_user(name=name, password=password)
    if not result:
        return web.json_response(status=500)

    del result["password"]

    return web.json_response(data=jsonable(result), status=200)


@authed
async def update_user(request: web.Request, auth_id: int):
    _id = int(request.match_info["user_id"])

    if auth_id != _id:
        return wrap_errors("You do not have access to this resource", status=403)

    user = await database.users.get_user(_id)
    if not user:
        return web.json_response(status=404)

    content: dict = await request.json()
    errors = []

    name = content.get("name")
    if not name:
        errors.append("'name' must not be empty")
    else:
        user = await database.users.get_user_by_name(name)
        if user and user["id"] != _id:
            errors.append(f"The name '{name}' is already taken")

    password = content.get("password")
    if not password:
        errors.append("'password' must not be empty")

    if errors:
        return wrap_errors(errors)

    result = await database.users.update_user(_id=_id, name=name, password=password)
    if not result:
        return web.json_response(status=500)

    del result["password"]

    return web.json_response(data=jsonable(result), status=200)


async def get_users(_: web.Request):
    users = await database.users.get_users()

    return web.json_response(data=jsonable(users), status=200)


@authed
async def get_user(_: web.Request, auth_id: int):
    user = await database.users.get_user(auth_id)
    del user["password"]

    return web.json_response(data=jsonable(user), status=200)
