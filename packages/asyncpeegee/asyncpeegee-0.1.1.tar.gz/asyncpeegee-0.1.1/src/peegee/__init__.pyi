from typing import Any
import asyncpg
import peegee

Connection = asyncpg.Connection[asyncpg.Record]
Pool = asyncpg.Pool[asyncpg.Record]

class WrappedPool:
    def __init__(self, pool: Pool) -> None: ...

async def create_pool(
    dsn: str | None = None,
    *args: list[Any],
    **kwargs: dict[str, Any],
) -> peegee.WrappedPool:
    ...

