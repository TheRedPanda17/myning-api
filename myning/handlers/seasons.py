from myning import database
from myning.utils.auth import authed, permissioned
from aiohttp import web

from myning.utils.errors import wrap_errors


@authed
async def get_seasons(*_, **__):
    seasons = await database.seasons.get_seasons()
    for season in seasons:
        season["start_dt"] = str(season["start_dt"])
        season["end_dt"] = str(season["end_dt"])
        season["created_dt"] = str(season["created_dt"])
        season["updated_dt"] = str(season["updated_dt"])

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

    season["start_dt"] = str(season["start_dt"])
    season["end_dt"] = str(season["end_dt"])
    season["created_dt"] = str(season["created_dt"])
    season["updated_dt"] = str(season["updated_dt"])

    return web.json_response(data=season, status=200)
