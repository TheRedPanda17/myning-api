import psycopg2
from myning import database


async def upsert_score(user_season_id: int, score: float):
    conn = await database.POOLS["default"].acquire()
    async with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
        sql = """
        INSERT INTO scores 
        VALUES (DEFAULT, %(user_season_id)s, %(score)s, CAST(NOW() AS date))
        ON CONFLICT (user_season_id, date) 
            DO UPDATE
            SET 
                score = %(score)s
        RETURNING *;
        """

        try:
            await cursor.execute(
                sql,
                {"user_season_id": user_season_id, "score": score},
            )
        except (psycopg2.DataError, psycopg2.IntegrityError) as e:
            print(e)
            return None
        return await cursor.fetchone()


async def get_score(user_season_id: int):
    conn = await database.POOLS["default"].acquire()
    async with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
        sql = """
        SELECT * 
        FROM scores 
        WHERE user_season_id = %(user_season_id)s
        ORDER BY date DESC
        """

        try:
            await cursor.execute(sql, {"user_season_id": user_season_id})
            return await cursor.fetchone()
        except (psycopg2.DataError, psycopg2.IntegrityError) as e:
            print(e)
            return None


async def get_scores(user_season_id: int):
    conn = await database.POOLS["default"].acquire()
    async with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
        sql = """
        SELECT * 
        FROM scores 
        WHERE user_season_id = %(user_season_id)s
        ORDER BY date DESC
        """

        try:
            await cursor.execute(sql, {"user_season_id": user_season_id})
            return await cursor.fetchall()
        except (psycopg2.DataError, psycopg2.IntegrityError) as e:
            print(e)
            return None


async def get_all_scores():
    conn = await database.POOLS["default"].acquire()
    async with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
        sql = """
        SELECT DISTINCT ON (user_season_id)
            id,
            score,
            date
        FROM scores
        ORDER BY user_season_id ASC, date DESC;
        """

        try:
            await cursor.execute(sql)
            return await cursor.fetchall()
        except (psycopg2.DataError, psycopg2.IntegrityError) as e:
            print(e)
            return None
