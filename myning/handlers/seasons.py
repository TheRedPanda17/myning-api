from myning import database
from myning.utils.auth import authed, permissioned
from aiohttp import web

from myning.utils.errors import wrap_errors
from myning.utils.transforming import jsonable


@authed
async def get_seasons(*_, **__):
    seasons = await database.seasons.get_seasons()
    seasons = [jsonable(season) for season in seasons]

    return web.json_response(data=seasons, status=200)


@authed
@permissioned("create_seasons")
async def create_season(request: web.Request, *_, **__):
    content: dict = await request.json()

    errors = []
    expected_keys = ["name", "start_dt", "end_dt"]
    for key in expected_keys:
        if not key in content.keys():
            errors.append(f"'{key}' must not be empty")

    if errors:
        return wrap_errors(errors)

    season = await database.seasons.create_season(
        name=content["name"],
        start_dt=content["start_dt"],
        end_dt=content["end_dt"],
    )

    if not season:
        return web.json_response(status=500)

    return web.json_response(data=jsonable(season), status=200)
