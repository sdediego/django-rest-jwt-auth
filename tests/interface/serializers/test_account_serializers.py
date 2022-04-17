# coding: utf-8

import pytest
from marshmallow.exceptions import ValidationError

from src.domain.services.account import generate_password_hash
from src.interface.serializers.account import (
    NewUserSerializer, TokenSerializer, UserLoginSerializer, UserRegisterSerializer)
from tests.fixtures import token, user


@pytest.mark.unit
def test_new_user_serializer(user):
    valid_data = NewUserSerializer().dump(user)
    assert len(valid_data) == 1
    assert valid_data['email'] == user.email


@pytest.mark.unit
def test_token_serializer_load(token):
    data = {
        'token': token.token
    }
    valid_data = TokenSerializer().load(data)
    assert valid_data['token'] == token.token
    assert 'payload' in valid_data
    assert isinstance(valid_data['payload'], dict)
    assert 'user_id' in valid_data['payload']
    assert 'exp' in valid_data['payload']
    assert 'iat' in valid_data['payload']


@pytest.mark.unit
def test_token_serializer_validation_error():
    data = {
        'token': 123456789
    }
    result = TokenSerializer().load(data)
    assert 'errors' in result


@pytest.mark.unit
def test_token_serializer_dump(token):
    valid_data = TokenSerializer().dump(token)
    assert valid_data['token'] == token.token


@pytest.mark.unit
def test_user_login_serializer(user):
    data = {
        'email': user.email,
        'password': user.password
    }
    valid_data = UserLoginSerializer().load(data)
    assert valid_data['email'] == data['email']
    assert valid_data['password'] == generate_password_hash(data['password'])


@pytest.mark.unit
def test_user_login_serializer_validation_error(user):
    data = {
        'email': user.email
    }
    result = UserLoginSerializer().load(data)
    assert 'errors' in result


def _test_user_register_serializer_validate_password(password, error_message):
    with pytest.raises(ValidationError) as err:
        UserRegisterSerializer().validate_password(password)
    assert error_message == str(err.value)


@pytest.mark.unit
def test_user_register_serializer_password_without_letters(user):
    password = user.password.replace('Password', '1234')
    error_message = 'Password should have at least two letters.'
    _test_user_register_serializer_validate_password(password, error_message)


@pytest.mark.unit
def test_user_register_serializer_password_without_numbers(user):
    password = user.password.replace('1234', 'Password')
    error_message = 'Password should have at least one numeral.'
    _test_user_register_serializer_validate_password(password, error_message)


@pytest.mark.unit
def test_user_register_serializer_password_without_lowercase_letter(user):
    password = user.password.upper()
    error_message = 'Password should have at least one lowercase letter.'
    _test_user_register_serializer_validate_password(password, error_message)


@pytest.mark.unit
def test_user_register_serializer_password_without_uppercase_letter(user):
    password = user.password.lower()
    error_message = 'Password should have at least one uppercase letter.'
    _test_user_register_serializer_validate_password(password, error_message)


@pytest.mark.unit
def test_user_register_serializer_password_without_special_character(user):
    password = user.password.replace('_', '')
    error_message = 'Password should have at least one special character: _$@#%'
    _test_user_register_serializer_validate_password(password, error_message)


@pytest.mark.unit
def test_user_register_serializer_check_passwords(user):
    data = {
        'password': user.password.lower(),
        'password2': user.password
    }
    error_message = 'Password fields do not match.'
    with pytest.raises(ValidationError) as err:
        UserRegisterSerializer().check_passwords(data)
    assert error_message == str(err.value)


@pytest.mark.unit
def test_user_register_serializer(user):
    data = {
        'email': user.email,
        'password': user.password,
        'password2': user.password
    }
    valid_data = UserRegisterSerializer().load(data)
    assert valid_data['email'] == data['email']
    assert valid_data['password'] == generate_password_hash(data['password'])
    assert 'password2' not in valid_data


@pytest.mark.unit
def test_user_register_serializer_validation_error(user):
    data = {
        'email': user.email,
        'password': user.password
    }
    result = UserRegisterSerializer().load(data)
    assert 'errors' in result
