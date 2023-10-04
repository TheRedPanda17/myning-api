from aiohttp import web

from myning import database
from myning.utils.auth import authed, permissioned
from myning.utils.errors import wrap_errors
from myning.utils.transforming import jsonable


@authed
@permissioned("view_users_permissions")
async def get_user_permissions(request: web.Request, *_, **__):
    _id = int(request.match_info["user_id"])

    permissions = await database.permissions.get_user_permissions(user_id=_id)
    permissions = [jsonable(permission) for permission in permissions]

    return web.json_response(data=permissions, status=200)


@authed
@permissioned("grant_users_permissions")
async def grant_user_permissions(request: web.Request, auth_id: int):
    user_id = int(request.match_info["user_id"])

    content: dict = await request.json()
    errors = []

    permission = content.get("permission")
    if not permission:
        errors.append("'permission' must not be empty")

    content_user_id = content.get("user_id")
    if not user_id or content_user_id != user_id:
        errors.append("'user_id' must not be empty and must match the path")

    if errors:
        return wrap_errors(errors)

    permission = await database.permissions.get_permission_by_name(permission)
    if not permission:
        return wrap_errors("No such permission", 404)

    user = await database.users.get_user(user_id)
    if not user:
        return wrap_errors("No such user", 404)

    result = await database.users_permissions.create_user_permission(
        permission_id=permission["id"], user_id=user_id, created_by=auth_id
    )
    if not result:
        return web.json_response(status=500)

    return web.json_response(data=jsonable(result), status=200)


@authed
@permissioned("revoke_users_permissions")
async def revoke_user_permissions(request: web.Request, auth_id: int):
    user_id = int(request.match_info["user_id"])
    permission_id = int(request.match_info["permission_id"])

    permission = await database.permissions.get_permission(permission_id)
    if not permission:
        return wrap_errors("No such permission", 404)

    user = await database.users.get_user(user_id)
    if not user:
        return wrap_errors("No such user", 404)

    user_permisson = await database.users_permissions.get_user_permission(
        user_id=user_id, permission_id=permission_id
    )
    if not user_permisson:
        return wrap_errors("User does not have this permission", 404)

    result = await database.users_permissions.revoke_user_permission(
        permission_id=permission_id, user_id=user_id, revoked_by=auth_id
    )
    if not result:
        return web.json_response(status=500)

    return web.json_response(data=jsonable(result), status=200)
