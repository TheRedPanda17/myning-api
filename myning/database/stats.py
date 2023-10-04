import psycopg2
from myning import database


async def get_stats(user_season_id: int):
    conn = await database.POOLS["default"].acquire()
    async with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
        sql = "SELECT * FROM stats WHERE user_season_id = %(user_season_id)s;"

        try:
            await cursor.execute(sql, {"user_season_id": user_season_id})
            return await cursor.fetchall()
        except (psycopg2.DataError, psycopg2.IntegrityError) as e:
            print(e)
            return None


async def upsert_stat(user_season_id: int, key: str, value: int):
    conn = await database.POOLS["default"].acquire()
    async with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
        sql = """
        INSERT INTO stats 
        VALUES (DEFAULT, %(user_season_id)s, %(key)s, %(value)s, NOW(), NOW())
        ON CONFLICT (user_season_id, key) 
            DO UPDATE
            SET 
                value = %(value)s,
                updated_dt = NOW()
        RETURNING *;
        """

        try:
            await cursor.execute(
                sql,
                {
                    "user_season_id": user_season_id,
                    "key": key,
                    "value": value,
                },
            )
        except (psycopg2.DataError, psycopg2.IntegrityError) as e:
            print(e)
            return None
        return await cursor.fetchone()


async def get_stat(user_season_id: int, key: str):
    conn = await database.POOLS["default"].acquire()
    async with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
        sql = """
        SELECT * 
        FROM stats 
        WHERE 
            user_season_id = %(user_season_id)s AND
            key = %(key)s"""

        try:
            await cursor.execute(sql, {"user_season_id": user_season_id, "key": key})
            return await cursor.fetchone()
        except (psycopg2.DataError, psycopg2.IntegrityError) as e:
            print(e)
            return None
