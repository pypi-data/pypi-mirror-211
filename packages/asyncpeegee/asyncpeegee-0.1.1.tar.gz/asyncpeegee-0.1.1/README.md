# peegee
a small typed wrapper around asyncpg for personal projects

## installation
```shell script
pip3 install asyncpeegee
```

## usage
```python
from peegee import create_pool, Pool

pool: Pool

pool = await peegee.create_pool("postgres://...")

# con is properly typed as peegee.Connection
async with pool.acquire() as con:
	await con.execute("SELECT 1=1")
```

## coverage
only the parts of the library i use

## support
none provided
