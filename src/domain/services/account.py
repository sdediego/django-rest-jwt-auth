# coding: utf-8

import hashlib
from datetime import datetime, timedelta

import jwt

from src.domain.entities.account import TokenEntity
from src.domain.exceptions import InvalidToken
from src.domain.services.constants import JWT_ALGORITHM, JWT_EXP_DELTA_SECONDS, JWT_KEY


def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, JWT_KEY, JWT_ALGORITHM)
    except jwt.DecodeError:
        raise InvalidToken(message='Token is invalid')
    except jwt.ExpiredSignatureError:
        raise InvalidToken(message='Token is expired')
    return payload


def encode_token(user_id: int) -> TokenEntity:
    payload = {
        'user_id': user_id,
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(seconds=JWT_EXP_DELTA_SECONDS)
    }
    token = jwt.encode(payload, JWT_KEY, JWT_ALGORITHM)
    return TokenEntity(token=token)


def generate_password_hash(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()
