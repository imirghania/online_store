from contextlib import AbstractAsyncContextManager
from typing import Callable, Type
from beanie import Document
from product_catalouge.repository.base_repository import Repository
from exceptions import NotAssignedRepository

NotAssignedRepositoryError = NotAssignedRepository(
    'Select a repository first using the get_repository method.'
    )


class UnitOfWork(AbstractAsyncContextManager):
    def __init__(self, repository: Repository):
        self.repository = repository

    async def commit(self):
        self.repository.model.save_changes()

    async def rollback(self):
        self.repository.model.rollback()

    async def __aexit__(self, exc_type, exc_value, traceback):
        if exc_type:
            await self.rollback()
        # else:
        #     await self.commit()