import psycopg2
from story import database


async def create_user_permission(permission_id: str, user_id: int, created_by: int):
    conn = await database.POOLS["default"].acquire()
    async with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
        sql = """
        INSERT INTO users_permissions 
        VALUES (%(permission_id)s, %(user_id)s, %(created_by)s, NOW())
        ON CONFLICT (user_id, permission_id) 
            DO UPDATE
            SET 
                created_by = %(user_id)s, 
                created_dt = NOW(), 
                revoked_by = NULL, 
                revoked_dt = NULL
        RETURNING *;
        """

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


async def get_user_permission(user_id: int, permission_id):
    conn = await database.POOLS["default"].acquire()
    async with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
        sql = """
        SELECT *
        FROM users_permissions
        WHERE user_id = %(user_id)s AND permission_id = %(permission_id)s
        """

        try:
            await cursor.execute(
                sql, {"user_id": user_id, "permission_id": permission_id}
            )
            return await cursor.fetchone()
        except (psycopg2.DataError, psycopg2.IntegrityError) as e:
            print(e)
            return None


async def revoke_user_permission(permission_id: str, user_id: int, revoked_by: int):
    conn = await database.POOLS["default"].acquire()
    async with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
        sql = """
        UPDATE users_permissions 
        SET revoked_by = %(revoked_by)s, revoked_dt = NOW()
        WHERE user_id = %(user_id)s AND permission_id = %(permission_id)s
        RETURNING *;
        """

        try:
            await cursor.execute(
                sql,
                {
                    "revoked_by": revoked_by,
                    "user_id": user_id,
                    "permission_id": permission_id,
                },
            )
        except (psycopg2.DataError, psycopg2.IntegrityError) as e:
            print(e)
            return None
        return await cursor.fetchone()
