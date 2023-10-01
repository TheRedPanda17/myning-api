from aiohttp import web

from story import database
from story.utils.auth import authed, permissioned

@authed
@permissioned("view_permissions")
async def get_permissions(*_, **__):
    permissions = await database.permissions.get_permissions()
    for permission in permissions:
        permission["created_dt"] = str(permission["created_dt"])
        permission["updated_dt"] = str(permission["updated_dt"])

    return web.json_response(data=permissions, status=200)
