from contextlib import AbstractAsyncContextManager
from repository.base_repository import Repository
from . import Service



class UnitOfWork(AbstractAsyncContextManager):
    def __init__(self, service: Service, repository: Repository):
        self.service = service(repository)
        self._changes = []

    async def commit(self):
        """Commit the changes by calling save_changes() on the service."""
        for change in self._changes:
            await change.save_changes()
        self._changes.clear()

    async def rollback(self):
        """Rollback the changes by calling rollback() on the service."""
        for change in self._changes:
            await change.rollback()
        self._changes.clear()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        if exc_type:
            await self.rollback()
        else:
            await self.commit()

    def track(self, *change):
        """Track a change made during the transaction."""
        self._changes + list(change)
