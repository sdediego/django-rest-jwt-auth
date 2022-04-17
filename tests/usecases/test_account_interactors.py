# coding: utf-8

from unittest.mock import Mock

import pytest

from src.domain.entities.account import UserEntity
from src.usecases.account import UserInteractor
from tests.fixtures import user


@pytest.mark.unit
def test_user_interactor_login(user):
    user_repo = Mock()
    user_repo.login.return_value = user
    user_interactor = UserInteractor(user_repo)
    result = user_interactor.login(user.email, user.password)
    assert user_repo.login.called
    assert isinstance(result, UserEntity)
    assert result.email == user.email


@pytest.mark.unit
def test_user_interactor_register(user):
    user_repo = Mock()
    user_repo.register.return_value = user
    user_interactor = UserInteractor(user_repo)
    result = user_interactor.register(user.email, user.password)
    assert user_repo.register.called
    assert isinstance(result, UserEntity)
    assert result.email == user.email
