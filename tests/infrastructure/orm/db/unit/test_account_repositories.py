# coding: utf-8

import dataclasses
from unittest.mock import patch

from django.db.utils import IntegrityError

import pytest

from src.domain.account import UserEntity
from src.domain.exceptions import DuplicateEntity
from src.infrastructure.orm.db.account.models import User
from src.infrastructure.orm.db.account.repositories import UserDatabaseRepository
from tests.fixtures import user


@pytest.mark.unit
@patch.object(User, 'objects')
def test_user_db_repository_create(mock_objects, user):
    mock_create = mock_objects.create
    mock_create.return_value = User(**dataclasses.asdict(user))
    result = UserDatabaseRepository().create(user.email, user.password)
    assert isinstance(user, UserEntity)
    assert result.email == user.email
    assert str(result) != str(user)


@pytest.mark.unit
@patch.object(User, 'objects')
def test_user_db_repository_create_duplicate(mock_objects, user):
    mock_create = mock_objects.create
    mock_create.side_effect = IntegrityError
    with pytest.raises(DuplicateEntity) as err:
        UserDatabaseRepository().create(user.email, user.password)
    assert 'Already exists a user with this data' in str(err.value)
