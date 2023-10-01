import psycopg2
from story import database

async def create_user_permission(permission_id: str, user_id: int, created_by: int):
    conn = await database.POOLS["default"].acquire()
    async with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
        sql = "INSERT INTO users_permissions VALUES (%(permission_id)s, %(user_id)s, %(created_by)s, NOW()) RETURNING *;"

        try:
            await cursor.execute(
                sql,
                {
                    "permission_id": permission_id,
                    "user_id": user_id,
                    "created_by": created_by,
                },
            )
        except (psycopg2.DataError, psycopg2.IntegrityError) as e:
            print(e)
            return None
        return await cursor.fetchone()
