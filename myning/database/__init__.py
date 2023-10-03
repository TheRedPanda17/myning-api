import asyncio
import aiopg

from . import users, permissions, users_permissions, seasons, users_seasons

POOLS: dict[str, aiopg.Pool] = {}


async def init(
    *,
    port=None,
    host=None,
    user=None,
    database=None,
    dsn=None,
    min_pool_size=1,
    max_pool_size=0,
    conn_timeout=5,
):
    dsn = f"dbname={database} user={user} host={host}"
    if port:
        dsn += f" port={port}"

    async with asyncio.Lock():
        POOLS[database] = await aiopg.create_pool(
            dsn,
            minsize=min_pool_size,
            maxsize=max_pool_size,
            timeout=conn_timeout,
        )

        POOLS["default"] = POOLS[database]


async def close():
    """Close postgresql connection pool(s). If no dbname is passed, all pools are closed."""

    await asyncio.gather(*(_close_pool(dbname) for dbname in POOLS))


async def _close_pool(dbname: str):
    """Close a single postgresql connection pool by dbname."""
    pool = POOLS.pop(dbname)
    pool.close()
    await pool.wait_closed()
