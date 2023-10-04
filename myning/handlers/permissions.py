from aiohttp import web

from myning import database
from myning.utils.auth import authed, permissioned
from myning.utils.errors import wrap_errors
from myning.utils.transforming import jsonable


@authed
@permissioned("view_permissions")
async def get_permissions(*_, **__):
    permissions = await database.permissions.get_permissions()
    permissions = [jsonable(permission) for permission in permissions]

    return web.json_response(data=permissions, status=200)
