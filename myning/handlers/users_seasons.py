from aiohttp import web
from myning import database

from myning.utils.auth import authed
from myning.utils.errors import wrap_errors
from myning.utils.transforming import jsonable


@authed
async def create_user_season(request: web.Request, auth_id: int, *_, **__):
    _id = int(request.match_info["user_id"])

    if auth_id != _id:
        return wrap_errors("You do not have access to this resource", status=403)

    content: dict = await request.json()

    errors = []
    expected_keys = ["user_id", "season_id"]

    for key in expected_keys:
        if not key in content.keys():
            errors.append(f"'{key}' must not be empty")

    if errors:
        return wrap_errors(errors)

    if content["user_id"] != auth_id:
        return wrap_errors("You cannot create someone else's user-season")

    user = await database.users.get_user(auth_id)
    if not user:
        return wrap_errors("User not found", status=404)

    season = await database.seasons.get_season(content["season_id"])
    if not season:
        return wrap_errors("Season not found", status=404)

    user_season = await database.users_seasons.create_user_season(
        season_id=content["season_id"], user_id=auth_id
    )

    return web.json_response(data=jsonable(user_season), status=200)
