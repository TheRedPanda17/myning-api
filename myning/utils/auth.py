import functools
from aiohttp import BasicAuth, web
from myning import database

from myning.utils.errors import wrap_errors


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


def permissioned(permissions: str | list[str]):
    if isinstance(permissions, str):
        permissions = [permissions]

    def decorator(func):
        """Permissions decorator function."""

        @functools.wraps(func)
        async def wrapper(request: web.Request, auth_id: int, *args, **kwargs):
            """Check permissions"""

            user_permissions = await database.permissions.get_user_permissions(auth_id)
            user_permissions = [permission["name"] for permission in user_permissions]
            if user_permissions is None:
                return web.json_response(status=500)

            for permission in permissions:
                if permission not in user_permissions:
                    return wrap_errors("You do not have access to this", status=403)

            return await func(request, auth_id=auth_id, *args, **kwargs)

        return wrapper

    return decorator
