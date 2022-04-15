# coding: utf-8

import dataclasses
from http import HTTPStatus
from unittest.mock import patch

from django.db.utils import IntegrityError
from django.urls import reverse

from src.infrastructure.orm.db.account.models import User
from tests.fixtures import user


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
