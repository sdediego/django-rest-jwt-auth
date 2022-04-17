# coding: utf-8

from datetime import datetime, timedelta

import jwt

from src.domain.account import UserEntity, UserTokenEntity
from src.domain.constants import JWT_ALGORITHM, JWT_EXP_DELTA_SECONDS, JWT_KEY


def generate_user_token(user: UserEntity) -> UserTokenEntity:
    payload = {
        'user_id': user.id,
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(seconds=JWT_EXP_DELTA_SECONDS)
    }
    token = jwt.encode(payload, JWT_KEY, JWT_ALGORITHM)
    return UserTokenEntity(user=user, token=token)
