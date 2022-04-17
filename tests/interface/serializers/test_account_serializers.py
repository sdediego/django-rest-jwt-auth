# coding: utf-8

import pytest
from marshmallow.exceptions import ValidationError

from src.domain.services.account import generate_password_hash
from src.interface.serializers.account import (
    NewUserSerializer, TokenSerializer, UserLoginSerializer, UserRegisterSerializer)
from tests.fixtures import user, token


@pytest.mark.unit
def test_new_user_serializer(user):
    serializer = NewUserSerializer()
    valid_data = serializer.dump(user)
    assert len(valid_data) == 1
    assert valid_data['email'] == user.email


@pytest.mark.unit
def test_token_serializer(token):
    serializer = TokenSerializer()
    valid_data = serializer.dump(token)
    assert valid_data['token'] == token.token


@pytest.mark.unit
def test_user_login_serializer(user):
    data = {
        'email': user.email,
        'password': user.password,
    }
    serializer = UserLoginSerializer()
    valid_data = serializer.load(data)
    assert valid_data['email'] == data['email']
    assert valid_data['password'] == generate_password_hash(data['password'])


@pytest.mark.unit
def test_user_login_serializer_validation_error(user):
    data = {
        'email': user.email,
    }
    serializer = UserLoginSerializer()
    result = serializer.load(data)
    assert 'errors' in result


def _test_user_register_serializer_validate_password(password, error_message):
    serializer = UserRegisterSerializer()
    with pytest.raises(ValidationError) as err:
        serializer.validate_password(password)
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
    serializer = UserRegisterSerializer()
    with pytest.raises(ValidationError) as err:
        serializer.check_passwords(data)
    assert error_message == str(err.value)


@pytest.mark.unit
def test_user_register_serializer(user):
    data = {
        'email': user.email,
        'password': user.password,
        'password2': user.password
    }
    serializer = UserRegisterSerializer()
    valid_data = serializer.load(data)
    assert valid_data['email'] == data['email']
    assert valid_data['password'] == generate_password_hash(data['password'])
    assert 'password2' not in valid_data


@pytest.mark.unit
def test_user_register_serializer_validation_error(user):
    data = {
        'email': user.email,
        'password': user.password,
    }
    serializer = UserRegisterSerializer()
    result = serializer.load(data)
    assert 'errors' in result
