from aiohttp import web

from config import CONFIG
from myning import database
from myning.routes import get_routes


async def startup(_):
    """Initalize connections on app startup."""
    await database.init(**CONFIG["postgres"])


async def cleanup(_):
    """Close connections on app cleanup."""
    await database.close()


def get_app():
    app = web.Application()
    app.add_routes(get_routes())
    app.on_startup.append(startup)
    app.on_cleanup.append(cleanup)
    return app
