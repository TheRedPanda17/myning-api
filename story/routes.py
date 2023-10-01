from story.handlers import monitoring, users


def init_routes(app):
    app.router.add_get("/ping", monitoring.ping)
    app.router.add_post("/users", users.create_user)
    app.router.add_get("/users", users.get_users)
    app.router.add_put("/users/{name}", users.update_user)
