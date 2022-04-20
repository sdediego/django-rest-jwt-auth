# coding: utf-8

from src.domain.entities.account import UserEntity


class UserInteractor:

    def __init__(self, user_repo: object):
        self.user_repo = user_repo

    def login(self, email: str, password: str) -> UserEntity:
        return self.user_repo.login(email, password)

    def register(self, email: str, password: str) -> UserEntity:
        return self.user_repo.register(email, password)

    def update(self, user_id: int) -> UserEntity:
        return self.user_repo.update(user_id)
