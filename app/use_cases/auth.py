from abc import ABC, abstractmethod

from app.repositories.auth_repository import (AuthRepositoryInterface,
                                              DuplicateUserError)
from app.utils.hash import get_password_hash, verify_password
from app.utils.token import create_access_token


class AuthUseCaseInterface(ABC):
    @abstractmethod
    async def register(self, username: str, email: str, password: str):
        raise NotImplementedError

    @abstractmethod
    async def login(self, username: str, password: str):
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

    async def login(self, username: str, password: str) -> str:
        user = await self.auth_repository.get_user_by_username(username)

        if user is None:
            raise UserNotFoundError("User not found")

        if not verify_password(password, user.password):
            raise UserPasswordMismatchError("Incorrect password")
        access_token = create_access_token(user.username)

        return access_token
