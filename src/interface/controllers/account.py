# coding: utf-8

import logging
from http import HTTPStatus
from typing import Tuple

from src.domain.exceptions import DuplicateEntity
from src.interface.serializers.account import NewUserSerializer, UserRegisterSerializer
from src.usecases.account import UserInteractor


logger = logging.getLogger(__name__)


class UserController:

    def __init__(self, user_interactor: UserInteractor):
        self.user_interactor = user_interactor

    def register(self, params: dict) -> Tuple[dict, int]:
        logger.info('Registering user with params: %s', str(params))
        data = UserRegisterSerializer().load(params)
        if 'errors' in data:
            logger.error('Error deserializing params: %s', str(data['errors']))
            return data, HTTPStatus.BAD_REQUEST.value
        try:
            user = self.user_interactor.register(**data)
        except DuplicateEntity as err:
            logger.error('Error creating duplicate user with params %s: %s', str(params), str(err))
            return {'error': str(err)}, HTTPStatus.BAD_REQUEST.value
        logger.info('User successfully created: %s', str(user))
        return NewUserSerializer().dump(user), HTTPStatus.CREATED.value
