# coding: utf-8

import logging
from http import HTTPStatus
from typing import Tuple

from src.domain.exceptions import EntityDoesNotExist, EntityDuplicate
from src.interface.controllers.utils import generate_user_token
from src.interface.serializers.account import (
    NewUserSerializer, UserLoginSerializer, UserRegisterSerializer, UserTokenSerializer)
from src.usecases.account import UserInteractor


logger = logging.getLogger(__name__)


class UserController:

    def __init__(self, user_interactor: UserInteractor):
        self.user_interactor = user_interactor

    def login(self, params: dict) -> Tuple[dict, int]:
        logger.info('Login user with params: %s', str(params))
        data = UserLoginSerializer().load(params)
        if 'errors' in data:
            logger.error('Error deserializing params: %s', str(data['errors']))
            return data, HTTPStatus.BAD_REQUEST.value
        try:
            user = self.user_interactor.login(**data)
        except EntityDoesNotExist as err:
            logger.error('Error login user with params %s: %s', str(params), err.message)
            return {'error': err.message}, HTTPStatus.BAD_REQUEST.value
        user_token = generate_user_token(user)
        logger.info('User successfully logged in: %s', str(user))
        return UserTokenSerializer().dump(user_token), HTTPStatus.OK.value

    def register(self, params: dict) -> Tuple[dict, int]:
        logger.info('Registering user with params: %s', str(params))
        data = UserRegisterSerializer().load(params)
        if 'errors' in data:
            logger.error('Error deserializing params: %s', str(data['errors']))
            return data, HTTPStatus.BAD_REQUEST.value
        try:
            user = self.user_interactor.register(**data)
        except EntityDuplicate as err:
            logger.error('Error creating duplicate user with params %s: %s', str(params), err.message)
            return {'error': err.message}, HTTPStatus.BAD_REQUEST.value
        logger.info('User successfully created: %s', str(user))
        return NewUserSerializer().dump(user), HTTPStatus.CREATED.value
