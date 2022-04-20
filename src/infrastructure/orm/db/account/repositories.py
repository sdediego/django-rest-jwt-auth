# coding: utf-8

from django.db.utils import IntegrityError
from django.utils import timezone

from src.domain.entities.account import UserEntity
from src.domain.exceptions import EntityDoesNotExist, EntityDuplicate
from src.infrastructure.orm.db.account.models import User


class UserDatabaseRepository:

    def create(self, email: str, password: str) -> UserEntity:
        try:
            user = User.objects.create(email=email, password=password)
        except IntegrityError:
            raise EntityDuplicate(message='Already exists a user with this data.')
        return user.map(fields=['id', 'email'])

    def get(self, email: str, password: str) -> UserEntity:
        try:
            user = User.objects.get(email=email, password=password)
        except User.DoesNotExist:
            raise EntityDoesNotExist(message='User does not exist with this data.')
        return user.map(fields=['id', 'username', 'email', 'is_active', 'last_login'])

    def update(self, user_id: int) -> UserEntity:
        user = User.objects.get(pk=user_id)
        user.last_login = timezone.now()
        user.save(update_fields=['last_login'])
        return user.map(fields=['id', 'username', 'email', 'is_active', 'last_login'])
