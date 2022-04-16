# coding: utf-8

from django.db.utils import IntegrityError

from src.domain.account import UserEntity
from src.domain.exceptions import EntityDoesNotExist, EntityDuplicate
from src.infrastructure.orm.db.account.models import User
from src.infrastructure.orm.db.account.utils import update_last_login


class UserDatabaseRepository:

    def create(self, email: str, password: str) -> UserEntity:
        try:
            user = User.objects.create(email=email, password=password)
        except IntegrityError as err:
            raise EntityDuplicate('Already exists a user with this data: %s', str(err))
        return user.map(fields=['email'])

    def get(self, email: str, password: str) -> UserEntity:
        try:
            user = User.objects.get(email=email, password=password)
        except User.DoesNotExist as err:
            raise EntityDoesNotExist('User does not exist with this data: %s', str(err))
        user = update_last_login(user)
        return user.map(fields=['id', 'username', 'email', 'is_active', 'last_login'])
