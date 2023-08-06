# peegee - a small typed wrapper around asyncpg for personal projects
# Copyright (C) 2023 Violet McKinney <opensource@viomck.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from typing import Any
import apgtypes
import asyncpg.pool

PoolAcquireContext = asyncpg.pool.PoolAcquireContext[asyncpg.Record]

class WrappedPoolAcquireContext:
	ctx: PoolAcquireContext
	
	def __init__(self, ctx: PoolAcquireContext):
		self.ctx = ctx

	async def __aenter__(self) -> apgtypes.Connection:
		return await self.ctx.__aenter__()  # type: ignore
	
	async def __aexit__(self, *exc: Any):
		await self.ctx.__aexit__(self, *exc)

	def __await__(self) -> Any:
		return self.ctx.__await__()
	

