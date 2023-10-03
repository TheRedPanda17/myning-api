import psycopg2
from myning import database


async def get_seasons():
    conn = await database.POOLS["default"].acquire()
    async with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
        sql = "SELECT * FROM seasons;"

        try:
            await cursor.execute(sql)
            return await cursor.fetchall()
        except (psycopg2.DataError, psycopg2.IntegrityError) as e:
            print(e)
            return None


async def create_season(name: str, start_dt, end_dt):
    conn = await database.POOLS["default"].acquire()
    async with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
        sql = """
        INSERT INTO seasons(name, start_dt, end_dt, created_dt, updated_dt) 
        VALUES(%(name)s, %(start_dt)s, %(end_dt)s, NOW(), NOW())
        RETURNING *;
        """

        try:
            await cursor.execute(
                sql, {"name": name, "start_dt": start_dt, "end_dt": end_dt}
            )
            return await cursor.fetchone()
        except (psycopg2.DataError, psycopg2.IntegrityError) as e:
            print(e)
            return None


async def get_season(_id: int):
    conn = await database.POOLS["default"].acquire()
    async with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
        sql = "SELECT * FROM seasons WHERE id = %(id)s;"

        try:
            await cursor.execute(sql, {"id": _id})
            return await cursor.fetchone()
        except (psycopg2.DataError, psycopg2.IntegrityError) as e:
            print(e)
            return None
