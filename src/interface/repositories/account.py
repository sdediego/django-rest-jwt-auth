# coding: utf-8

from src.domain.account import UserEntity


class UserRepository:

    def __init__(self, db_repo: object):
        self.db_repo = db_repo

    def register(self, email: str, password: str) -> UserEntity:
        return self.db_repo.create(email, password)
