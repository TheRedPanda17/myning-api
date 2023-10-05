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
