# coding: utf-8

from datetime import datetime, timedelta

from django.conf import settings

import jwt

from src.domain.account import UserEntity, UserTokenEntity


def generate_user_token(user: UserEntity) -> UserTokenEntity:
    payload = {
        'user_id': user.id,
        'expire': datetime.utcnow() + timedelta(seconds=settings.JWT_EXP_DELTA_SECONDS)
    }
    token = jwt.encode(payload, settings.JWT_KEY, settings.JWT_ALGORITHM).decode('utf-8')
    return UserTokenEntity(user=user, token=token)
