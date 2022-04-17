# coding: utf-8

from unittest.mock import Mock

import pytest

from src.domain.entities.account import UserEntity
from src.interface.repositories.account import UserRepository
from tests.fixtures import user


@pytest.mark.unit
def test_user_interactor_login(user):
    db_repo = Mock()
    db_repo.get.return_value = user
    user_repo = UserRepository(db_repo)
    result = user_repo.login(user.email, user.password)
    assert db_repo.get.called
    assert isinstance(result, UserEntity)
    assert result.email == user.email


@pytest.mark.unit
def test_user_interactor_register(user):
    db_repo = Mock()
    db_repo.create.return_value = user
    user_repo = UserRepository(db_repo)
    result = user_repo.register(user.email, user.password)
    assert db_repo.create.called
    assert isinstance(result, UserEntity)
    assert result.email == user.email
