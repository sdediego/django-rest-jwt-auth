# coding: utf-8

import dataclasses
from http import HTTPStatus
from unittest.mock import patch

from django.db.utils import IntegrityError
from django.urls import reverse

from src.infrastructure.orm.db.account.models import User
from tests.fixtures import token, user


@patch.object(User, 'save')
@patch.object(User, 'objects')
def test_user_viewset_login(mock_objects, mock_save, user, client):
    mock_get = mock_objects.get
    mock_get.return_value = User(**dataclasses.asdict(user))
    url = reverse('api:accounts-login')
    data = {
        'email': user.email,
        'password': user.password
    }
    response = client.post(url, data=data)
    assert mock_get.called
    assert mock_save.called
    assert hasattr(response, 'status_code')
    assert response.status_code == HTTPStatus.OK.value
    assert hasattr(response, 'data')
    assert isinstance(response.data, dict)
    assert 'token' in response.data


@patch.object(User, 'save')
@patch.object(User, 'objects')
def test_user_viewset_login_bad_request(mock_objects, mock_save, user, client):
    mock_get = mock_objects.get
    mock_get.return_value = User(**dataclasses.asdict(user))
    url = reverse('api:accounts-login')
    data = {
        'email': user.email
    }
    response = client.post(url, data=data)
    assert not mock_get.called
    assert not mock_save.called
    assert hasattr(response, 'status_code')
    assert response.status_code == HTTPStatus.BAD_REQUEST.value
    assert hasattr(response, 'data')
    assert isinstance(response.data, dict)
    assert 'errors' in response.data


@patch.object(User, 'save')
@patch.object(User, 'objects')
def test_user_viewset_login_does_not_exist(mock_objects, mock_save, user, client):
    mock_get = mock_objects.get
    mock_get.side_effect = User.DoesNotExist
    url = reverse('api:accounts-login')
    data = {
        'email': user.email,
        'password': user.password
    }
    response = client.post(url, data=data)
    assert mock_get.called
    assert not mock_save.called
    assert hasattr(response, 'status_code')
    assert response.status_code == HTTPStatus.BAD_REQUEST.value
    assert hasattr(response, 'data')
    assert isinstance(response.data, dict)
    assert 'error' in response.data


def test_user_viewset_refresh(token, client):
    headers= {'HTTP_Authorization': token.token}
    url = reverse('api:accounts-refresh')
    response = client.get(url, **headers)
    assert hasattr(response, 'status_code')
    assert response.status_code == HTTPStatus.OK.value
    assert hasattr(response, 'data')
    assert isinstance(response.data, dict)
    assert 'token' in response.data


def test_user_viewset_token_bad_request(client):
    headers= {'HTTP_Authorization': ''}
    url = reverse('api:accounts-refresh')
    response = client.get(url, **headers)
    assert hasattr(response, 'status_code')
    assert response.status_code == HTTPStatus.BAD_REQUEST.value
    assert hasattr(response, 'data')
    assert isinstance(response.data, dict)
    assert 'errors' in response.data


@patch.object(User, 'objects')
def test_user_viewset_register(mock_objects, user, client):
    mock_create = mock_objects.create
    mock_create.return_value = User(**dataclasses.asdict(user))
    url = reverse('api:accounts-register')
    data = {
        'email': user.email,
        'password': user.password,
        'password2': user.password
    }
    response = client.post(url, data=data)
    assert mock_create.called
    assert hasattr(response, 'status_code')
    assert response.status_code == HTTPStatus.CREATED.value
    assert hasattr(response, 'data')
    assert isinstance(response.data, dict)


@patch.object(User, 'objects')
def test_user_viewset_register_bad_request(mock_objects, user, client):
    mock_create = mock_objects.create
    mock_create.return_value = User(**dataclasses.asdict(user))
    url = reverse('api:accounts-register')
    data = {
        'email': user.email,
        'password': user.password,
        'password2': 'password2'
    }
    response = client.post(url, data=data)
    assert not mock_create.called
    assert hasattr(response, 'status_code')
    assert response.status_code == HTTPStatus.BAD_REQUEST.value
    assert hasattr(response, 'data')
    assert isinstance(response.data, dict)
    assert 'errors' in response.data


@patch.object(User, 'objects')
def test_user_viewset_register_duplicate(mock_objects, user, client):
    mock_create = mock_objects.create
    mock_create.side_effect = IntegrityError
    url = reverse('api:accounts-register')
    data = {
        'email': user.email,
        'password': user.password,
        'password2': user.password
    }
    response = client.post(url, data=data)
    assert mock_create.called
    assert hasattr(response, 'status_code')
    assert response.status_code == HTTPStatus.BAD_REQUEST.value
    assert hasattr(response, 'data')
    assert isinstance(response.data, dict)
    assert 'error' in response.data
