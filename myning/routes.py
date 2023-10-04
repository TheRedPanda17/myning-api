from aiohttp import web

from myning.handlers import (monitoring, permissions, seasons, users,
                             users_permissions, users_seasons)


def get_routes():
    return [
        web.get("/ping", monitoring.ping),
        # Users
        web.post("/users", users.create_user),
        web.get("/users", users.get_users),
        web.put("/users/{id}", users.update_user),
        # Permissions
        web.get("/permissions", permissions.get_permissions),
        # User Permissions
        web.get("/users/{id}/permissions", users_permissions.get_user_permissions),
        web.post("/users/{id}/permissions", users_permissions.grant_user_permissions),
        web.delete(
            "/users/{id}/permissions/{permission_id}",
            users_permissions.revoke_user_permissions,
        ),
        # Seasons
        web.get("/seasons", seasons.get_seasons),
        web.post("/seasons", seasons.create_season),
        # User Seasons
        web.post("/users/{id}/seasons", users_seasons.create_user_season),
    ]
