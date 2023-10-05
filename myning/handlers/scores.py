from myning import database
from myning.handlers.users_seasons import user_season
from myning.utils.auth import authed

from aiohttp import web
from myning.utils.errors import wrap_errors

from myning.utils.transforming import jsonable


@authed
@user_season
async def create_score(request: web.Request, user_season_id: int = None, *_, **__):
    content: dict = await request.json()
    score = content.get("score")
    if not score:
        return wrap_errors("'score' key must not be empty", status=400)

    score = await database.scores.upsert_score(
        user_season_id=user_season_id, score=score
    )

    return web.json_response(jsonable(score), status=200)


@authed
@user_season
async def get_score(req, user_season_id: int = None, *_, **__):
    score = await database.scores.get_score(user_season_id=user_season_id)
    if not score:
        return web.Response(status=404)

    return web.json_response(jsonable(score), status=200)


@authed
@user_season
async def get_scores(req, user_season_id: int = None, *_, **__):
    scores = await database.scores.get_scores(user_season_id=user_season_id)
    if not scores:
        return web.Response(status=204)

    return web.json_response(jsonable(scores), status=200)
