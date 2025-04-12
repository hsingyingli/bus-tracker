from abc import ABC, abstractmethod

from app.utils.hash import get_password_hash

from app.repositories.auth_repository import (AuthRepositoryInterface,
                                              DuplicateUserError)


class AuthUseCaseInterface(ABC):
    @abstractmethod
    async def register(self, username: str, email: str, password: str):
        raise NotImplementedError


class UserNotFoundError(Exception):
    pass


class UserPasswordMismatchError(Exception):
    pass


class RegisterUserError(Exception):
    pass


class AuthUseCase(AuthUseCaseInterface):
    def __init__(self, auth_repository: AuthRepositoryInterface):
        self.auth_repository = auth_repository

    async def register(self, username: str, email: str, password: str):
        hashed_password = get_password_hash(password)
        try:
            return await self.auth_repository.register(username, email, hashed_password)
        except DuplicateUserError:
            raise RegisterUserError("User with this username already exists")
