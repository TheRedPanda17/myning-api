from myning.handlers import monitoring, users, permissions, users_permissions, seasons


def init_routes(app):
    app.router.add_get("/ping", monitoring.ping)

    # Users
    app.router.add_post("/users", users.create_user)
    app.router.add_get("/users", users.get_users)
    app.router.add_put("/users/{id}", users.update_user)

    # Permissions
    app.router.add_get("/permissions", permissions.get_permissions)

    # User Permissions
    app.router.add_get(
        "/users/{id}/permissions", users_permissions.get_user_permissions
    )
    app.router.add_post(
        "/users/{id}/permissions", users_permissions.grant_user_permissions
    )
    app.router.add_delete(
        "/users/{id}/permissions/{permission_id}",
        users_permissions.revoke_user_permissions,
    )

    # Seasons
    app.router.add_get("/seasons", seasons.get_seasons)
    app.router.add_post("/seasons", seasons.create_season)
