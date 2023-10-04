from myning import database
from myning.handlers.users_seasons import user_season
from myning.utils.auth import authed

from aiohttp import web
from myning.utils.errors import wrap_errors

from myning.utils.transforming import jsonable


@authed
@user_season
async def get_stats(*_, user_season_id: int = None, **__):
    stats = await database.stats.get_stats(user_season_id)
    stats = {stat["key"]: stat["value"] for stat in stats}
    if not stats:
        return web.Response(status=204)

    return web.json_response(data=stats, status=200)


@authed
@user_season
async def sync_stats(request: web.Request, user_season_id: int = None, *_, **__):
    content: dict = await request.json()

    data = {}
    for key, value in content.items():
        stat = await database.stats.upsert_stat(
            user_season_id=user_season_id, key=key, value=value
        )
        if not stat:
            return web.Request(status=500)
        data[stat["key"]] = stat["value"]

    return web.json_response(data, status=200)


@authed
@user_season
async def update_stat(request: web.Request, user_season_id: int = None, *_, **__):
    content: dict = await request.json()

    errors = []
    expected_keys = ["key", "value"]
    for key in expected_keys:
        if not key in content.keys():
            errors.append(f"'{key}' must not be empty")

    if errors:
        return wrap_errors(errors)

    stat = await database.stats.upsert_stat(
        user_season_id=user_season_id, key=content["key"], value=content["value"]
    )

    return web.json_response(jsonable(stat), status=200)


@authed
@user_season
async def increment_stat(request: web.Request, user_season_id: int = None, *_, **__):
    key = request.match_info["key"]

    stat = await database.stats.get_stat(user_season_id=user_season_id, key=key)
    if not stat:
        return web.Response(status=404)

    value = stat["value"] + 1

    stat = await database.stats.upsert_stat(
        user_season_id=user_season_id, key=key, value=value
    )

    return web.json_response(jsonable(stat), status=200)
