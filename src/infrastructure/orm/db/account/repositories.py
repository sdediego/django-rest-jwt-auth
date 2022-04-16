# coding: utf-8

from django.db.utils import IntegrityError

from src.domain.account import UserEntity
from src.domain.exceptions import EntityDuplicate
from src.infrastructure.orm.db.account.models import User


class UserDatabaseRepository:

    def create(self, email: str, password: str) -> UserEntity:
        try:
            user = User.objects.create(email=email, password=password)
        except IntegrityError as err:
            raise EntityDuplicate('Already exists a user with this data: %s', str(err))
        return user.map(fields=['email'])
