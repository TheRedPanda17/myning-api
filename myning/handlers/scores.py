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
