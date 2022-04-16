# coding: utf-8

from src.domain.account import UserEntity, UserTokenEntity


class UserRepository:

    def __init__(self, db_repo: object):
        self.db_repo = db_repo

    def login(self, email: str, password: str) -> UserTokenEntity:
        return self.db_repo.get(email, password)

    def register(self, email: str, password: str) -> UserEntity:
        return self.db_repo.create(email, password)
