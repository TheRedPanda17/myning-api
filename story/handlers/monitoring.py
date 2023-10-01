from aiohttp import web
import psycopg2

from story import database


async def ping(_):
    response = {"up": [], "down": [], "tables": []}
    conn = await database.POOLS["default"].acquire()
    async with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
        await cursor.execute("SELECT 1+1 AS sum;")
        result = await cursor.fetchone()
        if result["sum"] == 2:
            response["up"].append("postgres")

    return web.json_response(data=response, status=200)
