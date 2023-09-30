from aiohttp import web
from story.routes import init_routes
from story.config import get_config
from story import database


def init_config(app: web.Application, argv=None) -> None:
    app["config"] = get_config(argv)


async def init_database(app: web.Application) -> None:
    """
    This is signal for success creating connection with database
    """
    config = app["config"]["postgres"]
    await database.init(**config)


async def close_database(app: web.Application) -> None:
    """
    This is signal for success closing connection with database before shutdown
    """
    app["db"].close()
    await app["db"].wait_closed()


def init_app(argv=None) -> web.Application:
    app = web.Application()
    init_routes(app)
    init_config(app, argv)

    app.on_startup.extend([init_database])
    app.on_cleanup.extend([close_database])
    return app


app = init_app()
