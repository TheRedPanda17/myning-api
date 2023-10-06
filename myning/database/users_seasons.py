import psycopg2
from myning import database


async def create_user_season(user_id: str, season_id: int):
    conn = await database.POOLS["default"].acquire()
    async with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
        sql = """
        INSERT INTO users_seasons
        VALUES (DEFAULT, %(user_id)s, %(season_id)s, NOW(), NOW())
        ON CONFLICT (user_id, season_id) DO
            UPDATE SET updated_dt = NOW()
        RETURNING *;
        """

        try:
            await cursor.execute(
                sql,
                {
                    "user_id": user_id,
                    "season_id": season_id,
                },
            )
        except (psycopg2.DataError, psycopg2.IntegrityError) as e:
            print(e)
            return None
        return await cursor.fetchone()


async def get_user_season(user_id: int, season_id):
    conn = await database.POOLS["default"].acquire()
    async with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
        sql = """
        SELECT *
        FROM users_seasons
        WHERE user_id = %(user_id)s AND season_id = %(season_id)s
        """

        try:
            await cursor.execute(sql, {"user_id": user_id, "season_id": season_id})
            return await cursor.fetchone()
        except (psycopg2.DataError, psycopg2.IntegrityError) as e:
            print(e)
            return None


async def get_user_seasons(user_id: int):
    conn = await database.POOLS["default"].acquire()
    async with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
        sql = """
        SELECT s.*
        FROM users_seasons AS us JOIN seasons AS s ON us.season_id = s.id
        WHERE user_id = %(user_id)s
        """

        try:
            await cursor.execute(sql, {"user_id": user_id})
            return await cursor.fetchall()
        except (psycopg2.DataError, psycopg2.IntegrityError) as e:
            print(e)
            return None
