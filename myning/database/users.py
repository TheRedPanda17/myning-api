import psycopg2
from myning import database


async def create_user(name: str, password: str):
    conn = await database.POOLS["default"].acquire()
    async with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
        sql = "INSERT INTO users VALUES (DEFAULT, %(name)s, %(password)s, NOW(), NOW()) RETURNING *;"

        try:
            await cursor.execute(sql, {"name": name, "password": password})
        except (psycopg2.DataError, psycopg2.IntegrityError) as e:
            print(e)
            return None
        return await cursor.fetchone()


async def update_user(_id: int, name: str, password: str):
    conn = await database.POOLS["default"].acquire()
    async with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
        sql = """
        UPDATE users 
        SET name = %(name)s, password = %(password)s, updated_dt = NOW() 
        WHERE id = %(id)s
        RETURNING *;"""

        try:
            await cursor.execute(sql, {"name": name, "password": password, "id": _id})
        except (psycopg2.DataError, psycopg2.IntegrityError) as e:
            print(e)
            return None
        return await cursor.fetchone()


async def get_user(_id: int):
    conn = await database.POOLS["default"].acquire()
    async with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
        sql = "SELECT * FROM users WHERE id = %(id)s;"

        try:
            await cursor.execute(sql, {"id": _id})
            return await cursor.fetchone()
        except (psycopg2.DataError, psycopg2.IntegrityError) as e:
            print(e)
            return None


async def get_user_by_name(name: str):
    conn = await database.POOLS["default"].acquire()
    async with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
        sql = "SELECT * FROM users WHERE name = %(name)s;"

        try:
            await cursor.execute(sql, {"name": name})
            return await cursor.fetchone()
        except (psycopg2.DataError, psycopg2.IntegrityError) as e:
            print(e)
            return None


async def get_users():
    conn = await database.POOLS["default"].acquire()
    async with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
        sql = "SELECT id, name, created_dt, updated_dt FROM users;"

        try:
            await cursor.execute(sql)
            return await cursor.fetchall()
        except (psycopg2.DataError, psycopg2.IntegrityError) as e:
            print(e)
            return None
