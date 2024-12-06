from contextlib import AbstractAsyncContextManager
from typing import Callable, Type
from beanie import Document
from product_catalouge.repository.base_repository import Repository
from exceptions import NotAssignedRepository

NotAssignedRepositoryError = NotAssignedRepository(
    'Select a repository first using the get_repository method.'
    )


class UnitOfWork(AbstractAsyncContextManager):
    def __init__(self, repository_factory: Callable[[Type[Document]], Repository]):
        self.repository_factory = repository_factory
        self.repositories = {}
        self.current_repo = None

    def get_repository(self, model: Type[Document]):
        if model not in self.repositories:
            self.repositories[model] = self.repository_factory(model)
            self.current_repo = self.repositories[model]
        return self.current_repo

    async def commit(self):
        if self.current_repo is None:
            raise NotAssignedRepositoryError
        self.current_repo.model.save_changes()

    async def rollback(self):
        if self.current_repo is None:
            raise NotAssignedRepositoryError
        self.current_repo.model.rollback()

    async def __aexit__(self, exc_type, exc_value, traceback):
        if exc_type:
            await self.rollback()
        # else:
        #     await self.commit()