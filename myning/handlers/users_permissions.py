from aiohttp import web

from myning import database
from myning.utils.auth import authed, permissioned
from myning.utils.errors import wrap_errors


@authed
@permissioned("view_users_permissions")
async def get_user_permissions(request: web.Request, *_, **__):
    _id = request.path_qs.split("/")[-2]
    if _id.isdigit():
        _id = int(_id)
    else:
        return wrap_errors("'id' must be an integer")

    permissions = await database.permissions.get_user_permissions(user_id=_id)
    for permission in permissions:
        permission["created_dt"] = str(permission["created_dt"])

    return web.json_response(data=permissions, status=200)


@authed
@permissioned("grant_users_permissions")
async def grant_user_permissions(request: web.Request, auth_id: int):
    _id = request.path_qs.split("/")[-2]
    if _id.isdigit():
        _id = int(_id)
    else:
        return wrap_errors("'id' must be an integer")

    content: dict = await request.json()
    errors = []

    permission = content.get("permission")
    if not permission:
        errors.append("'permission' must not be empty")

    user_id = content.get("user_id")
    if not user_id:
        errors.append("'user_id' must not be empty")

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

    result["created_dt"] = str(result["created_dt"])
    result["revoked_dt"] = str(result["revoked_dt"])

    return web.json_response(data=result, status=200)


@authed
@permissioned("revoke_users_permissions")
async def revoke_user_permissions(request: web.Request, auth_id: int):
    user_id = request.path_qs.split("/")[-3]
    if user_id.isdigit():
        user_id = int(user_id)
    else:
        return wrap_errors("user id must be an integer")

    permission_id = request.path_qs.split("/")[-1]
    if permission_id.isdigit():
        permission_id = int(permission_id)
    else:
        return wrap_errors("permission id must be an integer")

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

    result["created_dt"] = str(result["created_dt"])
    result["revoked_dt"] = str(result["revoked_dt"])

    return web.json_response(data=result, status=200)
