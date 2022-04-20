# coding: utf-8

from datetime import datetime, timedelta

import pytest

from src.domain.entities.account import UserEntity
from src.domain.exceptions import EntityDoesNotExist, EntityDuplicate
from src.infrastructure.orm.db.account.repositories import UserDatabaseRepository
from tests.fixtures import user
from tests.infrastructure.orm.db.factories import UserFactory


@pytest.mark.django_db
def test_user_db_repository_create(user):
    result = UserDatabaseRepository().create(user.email, user.password)
    assert isinstance(user, UserEntity)
    assert result.email == user.email
    assert str(result) != str(user)


@pytest.mark.django_db
def test_user_db_repository_create_duplicate(user):
    UserFactory.create(email=user.email, password=user.password)
    with pytest.raises(EntityDuplicate) as err:
        UserDatabaseRepository().create(user.email, user.password)
    assert 'Already exists a user with this data' in str(err.value)


@pytest.mark.django_db
def test_user_db_repository_get(user):
    instance = UserFactory.create(
        email=user.email, password=user.password, last_login=user.last_login)
    result = UserDatabaseRepository().get(user.email, user.password)
    assert isinstance(user, UserEntity)
    assert result.email == user.email


@pytest.mark.django_db
def test_user_db_repository_get_does_not_exist():
    with pytest.raises(EntityDoesNotExist) as err:
        UserDatabaseRepository().get('user@email.com', 'password')
    assert 'User does not exist with this data' in str(err.value)


@pytest.mark.django_db
def test_user_db_repository_update(user):
    last_login = datetime.utcnow() + timedelta(days=-1)
    instance = UserFactory.create(
        email=user.email, password=user.password, last_login=last_login)
    result = UserDatabaseRepository().update(instance.id)
    assert isinstance(user, UserEntity)
    assert result.email == user.email
    assert result.last_login != instance.last_login
