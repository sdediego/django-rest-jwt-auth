# coding: utf-8

import pytest

from src.domain.account import UserEntity, UserTokenEntity
from src.interface.controllers.utils import generate_user_token
from tests.fixtures import user


@pytest.mark.unit
def test_generate_user_token(user):
    user_token = generate_user_token(user)
    assert isinstance(user_token, UserTokenEntity)
    assert hasattr(user_token, 'user')
    assert hasattr(user_token, 'token')
    assert isinstance(user_token.user, UserEntity)
    assert isinstance(user_token.token, str)
