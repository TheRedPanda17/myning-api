from story.handlers import monitoring


def init_routes(app):
    app.router.add_get("/ping", monitoring.ping)
