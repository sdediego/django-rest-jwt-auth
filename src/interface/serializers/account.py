# coding: utf-8

import hashlib
import re

from marshmallow import Schema, fields, validate, validates, validates_schema, EXCLUDE
from marshmallow.decorators import post_load
from marshmallow.exceptions import ValidationError


class NewUserSerializer(Schema):
    email = fields.Email(required=True)

    class Meta:
        unknown = EXCLUDE


class UserRegisterSerializer(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=8, max=20))
    password2 = fields.String(required=True, validate=validate.Length(min=8, max=20))

    @staticmethod
    def _validate_password(value: str):
        if not any(char.isalpha() for char in value):
            raise ValidationError('Password should have at least two letters.')
        if not any(char.isdigit() for char in value):
            raise ValidationError('Password should have at least one numeral.')
        if not any(char.islower() for char in value):
            raise ValidationError('Password should have at least one lowercase letter.')
        if not any(char.isupper() for char in value):
            raise ValidationError('Password should have at least one uppercase letter.')
        if re.search('[_$@#%]', value) is None:
            raise ValidationError('Password should have at least one special character: _$@#%')

    @validates('password')
    def validate_password(self, value: str):
        self._validate_password(value)

    @validates('password2')
    def validate_password(self, value: str):
        self._validate_password(value)

    @validates_schema
    def check_passwords(self, data: dict, **kwargs):
        if data['password'] != data['password2']:
            raise ValidationError('Password fields do not match.')

    def load(self, data: dict) -> dict:
        try:
            data = super().load(data)
        except ValidationError as err:
            data = {'errors': err.messages}
        return data

    @staticmethod
    def generate_password_hash(password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    @post_load
    def make_password_hash(self, data: dict, **kwargs) -> dict:
        data.pop('password2')
        data['password'] = self.generate_password_hash(data['password'])
        return data
