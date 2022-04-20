# coding: utf-8

from src.domain.entities.account import UserEntity


class UserRepository:

    def __init__(self, db_repo: object):
        self.db_repo = db_repo

    def login(self, email: str, password: str) -> UserEntity:
        return self.db_repo.get(email, password)

    def register(self, email: str, password: str) -> UserEntity:
        return self.db_repo.create(email, password)

    def update(self, user_id: int) -> UserEntity:
        return self.db_repo.update(user_id)
