# coding: utf-8

import pytest

from src.domain.entities.account import TokenEntity
from src.domain.services.account import (
    decode_token, encode_token, generate_password_hash)
from tests.fixtures import token, user


@pytest.mark.unit
def test_decode_token(token):
    payload = decode_token(token.token)
    assert isinstance(payload, dict)
    assert 'exp' in payload
    assert 'iat' in payload
    assert 'user_id' in payload


@pytest.mark.unit
def test_encode_token(user):
    token = encode_token(user.id)
    assert isinstance(token, TokenEntity)
    assert hasattr(token, 'token')
    assert isinstance(token.token, str)


@pytest.mark.unit
def test_generate_password_hash():
    password = 'Password_1234'
    hashed = generate_password_hash(password)
    assert isinstance(hashed, str)
    assert len(hashed) == 64
