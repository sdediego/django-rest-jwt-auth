# coding: utf-8

from unittest.mock import Mock

import pytest

from src.domain.entities.account import UserEntity
from src.interface.repositories.account import UserRepository
from tests.fixtures import user


@pytest.mark.unit
def test_user_repo_login(user):
    db_repo = Mock()
    db_repo.get.return_value = user
    user_repo = UserRepository(db_repo)
    result = user_repo.login(user.email, user.password)
    assert db_repo.get.called
    assert isinstance(result, UserEntity)
    assert result.email == user.email


@pytest.mark.unit
def test_user_repo_register(user):
    db_repo = Mock()
    db_repo.create.return_value = user
    user_repo = UserRepository(db_repo)
    result = user_repo.register(user.email, user.password)
    assert db_repo.create.called
    assert isinstance(result, UserEntity)
    assert result.email == user.email


@pytest.mark.unit
def test_user_repo_update(user):
    db_repo = Mock()
    db_repo.update.return_value = user
    user_repo = UserRepository(db_repo)
    result = user_repo.update(user.id)
    assert db_repo.update.called
    assert isinstance(result, UserEntity)
    assert result.email == user.email
