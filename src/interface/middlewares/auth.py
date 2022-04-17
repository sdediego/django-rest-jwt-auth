# coding: utf-8

import logging
from functools import wraps
from http import HTTPStatus
from typing import Callable, Tuple

from src.domain.exceptions import InvalidToken
from src.domain.services.account import decode_token


logger = logging.getLogger(__name__)


def auth_required(fn: Callable) -> Tuple[dict, int]:
    @wraps(fn)
    def decode_auth_token(*args, **kwargs) -> Tuple[dict, int]:
        token = kwargs.get('token', '')
        logger.info('Validating auth token: %s', token)
        if not token:
            logger.warning('Required auth token not found.')
            return None, HTTPStatus.UNAUTHORIZED.value
        try:
            decode_token(token)
        except InvalidToken as err:
            logger.warning('Invalid auth token: %s', token)
            return {'error': f'{err.message}: {token}'}, HTTPStatus.UNAUTHORIZED.value
        return fn(*args, **kwargs)
    return decode_auth_token
