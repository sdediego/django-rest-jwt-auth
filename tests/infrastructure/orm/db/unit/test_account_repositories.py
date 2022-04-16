# coding: utf-8

import dataclasses
from unittest.mock import patch

from django.db.utils import IntegrityError

import pytest

from src.domain.account import UserEntity
from src.domain.exceptions import EntityDoesNotExist, EntityDuplicate
from src.infrastructure.orm.db.account.models import User
from src.infrastructure.orm.db.account.repositories import UserDatabaseRepository
from tests.fixtures import user


@pytest.mark.unit
@patch.object(User, 'objects')
def test_user_db_repository_create(mock_objects, user):
    mock_create = mock_objects.create
    mock_create.return_value = User(**dataclasses.asdict(user))
    result = UserDatabaseRepository().create(user.email, user.password)
    assert mock_create.called
    assert isinstance(result, UserEntity)
    assert result.email == user.email


@pytest.mark.unit
@patch.object(User, 'objects')
def test_user_db_repository_create_duplicate(mock_objects, user):
    mock_create = mock_objects.create
    mock_create.side_effect = IntegrityError
    with pytest.raises(EntityDuplicate) as err:
        UserDatabaseRepository().create(user.email, user.password)
    assert mock_create.called
    assert 'Already exists a user with this data' in str(err.value)


@pytest.mark.unit
@patch.object(User, 'save')
@patch.object(User, 'objects')
def test_user_db_repository_get(mock_objects, mock_save, user):
    mock_get = mock_objects.get
    mock_get.return_value = User(**dataclasses.asdict(user))
    result = UserDatabaseRepository().get(user.email, user.password)
    assert mock_get.called
    assert mock_save.called
    assert isinstance(result, UserEntity)
    assert result.email == user.email
    assert result.last_login != user.last_login


@pytest.mark.unit
@patch.object(User, 'objects')
def test_user_db_repository_get_does_not_exist(mock_objects, user):
    mock_get = mock_objects.get
    mock_get.side_effect = User.DoesNotExist
    with pytest.raises(EntityDoesNotExist) as err:
        UserDatabaseRepository().get(user.email, user.password)
    assert mock_get.called
    assert 'User does not exist with this data' in str(err.value)
