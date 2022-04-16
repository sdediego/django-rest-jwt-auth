# coding: utf-8

import pytest

from src.domain.account import UserEntity
from src.domain.exceptions import EntityDuplicate
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
