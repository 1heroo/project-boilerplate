from types import TracebackType

from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.interfaces.persistence import IUnitOfWork


class UnitOfWork(IUnitOfWork):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def __aenter__(self) -> 'UnitOfWork':
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        if exc_type:
            await self.rollback()
        else:
            await self.commit()

    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self) -> None:
        await self._session.rollback()

    async def flush(self) -> None:
        await self._session.flush()
