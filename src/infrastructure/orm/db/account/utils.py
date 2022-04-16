# coding: utf-8

from django.utils import timezone

from src.infrastructure.orm.db.account.models import User


def update_last_login(user: User) -> User:
    user.last_login = timezone.now()
    user.save(update_fields=['last_login'])
    return user
