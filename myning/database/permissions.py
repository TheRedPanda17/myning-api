import psycopg2
from myning import database


async def create_permission(name: str):
    conn = await database.POOLS["default"].acquire()
    async with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
        sql = "INSERT INTO permissions VALUES (DEFAULT, %(name)s, NOW(), NOW()) ON CONFLICT DO NOTHING RETURNING *;"

        try:
            await cursor.execute(sql, {"name": name})
        except (psycopg2.DataError, psycopg2.IntegrityError) as e:
            print(e)
            return None
        return await cursor.fetchone()


async def get_permissions():
    conn = await database.POOLS["default"].acquire()
    async with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
        sql = "SELECT * FROM permissions;"

        try:
            await cursor.execute(sql)
            return await cursor.fetchall()
        except (psycopg2.DataError, psycopg2.IntegrityError) as e:
            print(e)
            return None


async def get_permission(_id: int):
    conn = await database.POOLS["default"].acquire()
    async with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
        sql = "SELECT * FROM permissions WHERE id = %(id)s;"

        try:
            await cursor.execute(sql, {"id": _id})
            return await cursor.fetchone()
        except (psycopg2.DataError, psycopg2.IntegrityError) as e:
            print(e)
            return None


async def get_permission_by_name(name: str):
    conn = await database.POOLS["default"].acquire()
    async with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
        sql = "SELECT * FROM permissions WHERE name = %(name)s;"

        try:
            await cursor.execute(sql, {"name": name})
            return await cursor.fetchone()
        except (psycopg2.DataError, psycopg2.IntegrityError) as e:
            print(e)
            return None


async def get_user_permissions(user_id: int):
    conn = await database.POOLS["default"].acquire()
    async with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
        sql = """
        SELECT p.name, up.created_dt, up.created_by
        FROM users_permissions AS up 
        JOIN permissions AS p on up.permission_id = p.id
        WHERE user_id = %(user_id)s AND revoked_dt IS NULL;
        """

        try:
            await cursor.execute(sql, {"user_id": user_id})
            return await cursor.fetchall()
        except (psycopg2.DataError, psycopg2.IntegrityError) as e:
            print(e)
            return None
