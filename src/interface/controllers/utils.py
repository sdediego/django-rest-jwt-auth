# coding: utf-8

from datetime import datetime, timedelta

from django.conf import settings

import jwt

from src.domain.account import UserEntity, UserTokenEntity


def generate_user_token(user: UserEntity) -> UserTokenEntity:
    expire = datetime.utcnow() + timedelta(seconds=settings.JWT_EXP_DELTA_SECONDS)
    payload = {
        'user_id': str(user.id),
        'expire': expire.strftime('%Y-%m-%d %H:%M:%S')
    }
    token = jwt.encode(payload, settings.JWT_KEY, settings.JWT_ALGORITHM)
    return UserTokenEntity(user=user, token=token)
