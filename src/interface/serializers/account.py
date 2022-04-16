# coding: utf-8

import re
from datetime import datetime

from marshmallow import Schema, fields, validate, validates, validates_schema, EXCLUDE
from marshmallow.decorators import post_load
from marshmallow.exceptions import ValidationError

from src.interface.serializers.utils import generate_password_hash


class NewUserSerializer(Schema):
    email = fields.Email(required=True)

    class Meta:
        unknown = EXCLUDE


class UserLoginSerializer(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)

    def load(self, data: dict) -> dict:
        try:
            data = super().load(data)
        except ValidationError as err:
            data = {'errors': err.messages}
        return data

    @post_load
    def make_password_hash(self, data: dict, **kwargs) -> dict:
        data['password'] = generate_password_hash(data['password'])
        return data


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

    @post_load
    def make_password_hash(self, data: dict, **kwargs) -> dict:
        data.pop('password2')
        data['password'] = generate_password_hash(data['password'])
        return data


class UserSerializer(Schema):
    id = fields.Integer()
    name = fields.String()
    surname = fields.String()
    username = fields.String()
    email = fields.Email(required=True)
    is_active = fields.Boolean(required=True)
    last_login = fields.String(required=True)
    date_joined = fields.String()

    @staticmethod
    def _validate_datetime(value: str, **kwags):
        try:
            datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            field_name = kwags.get('field_name')
            raise ValidationError(f'{field_name} field is not datetime string.')

    @validates('last_login')
    def validate_datetime(self, value: str, **kwargs):
        self._validate_datetime(value, **kwargs)

    @validates('date_joined')
    def validate_datetime(self, value: str, **kwargs):
        self._validate_datetime(value, **kwargs)


class UserTokenSerializer(Schema):
    token = fields.String(required=True)
    user = fields.Nested(UserSerializer, required=True)
