import functools
from aiohttp import BasicAuth, web
from story import database

from story.utils.errors import wrap_errors


def authed(func):
    """Auth decorator function."""

    @functools.wraps(func)
    async def wrapper(request: web.Request, *args, **kwargs):
        """Performs analysis of header"""

        encoded = request.headers.get("Authorization")
        if not encoded:
            return wrap_errors("Missing Authorization header", status=401)

        try:
            auth = BasicAuth.decode(encoded)
            print(auth)
        except Exception as e:
            print(e)
            return web.json_response(status=401, data="Invalid Authorization header")

        user = await database.users.get_user_by_name(auth.login)
        if not user:
            return web.json_response(status=401, data="Invalid auth user")

        if user["password"] != auth.password:
            return web.json_response(status=401, data="Invalid password")

        return await func(request, auth_id=user["id"], *args, **kwargs)

    return wrapper
