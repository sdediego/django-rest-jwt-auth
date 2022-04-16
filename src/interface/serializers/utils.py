# coding: utf-8

import hashlib


def generate_password_hash(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()
