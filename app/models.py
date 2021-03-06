from sqlalchemy import UniqueConstraint

from . import db
import datetime
from sqlalchemy.dialects.postgresql import UUID
from app.encryption import (
    hashpw,
    check_hash
)


def filter_null_value_fields(obj):
    return dict(
        filter(lambda x: x[1] is not None, obj.items())
    )


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, index=True, unique=False)
    email_address = db.Column(db.String(255), nullable=False, index=True, unique=True)
    created_at = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=False,
        default=datetime.datetime.now)
    updated_at = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=True,
        onupdate=datetime.datetime.now)
    _password = db.Column(db.String, index=False, unique=False, nullable=False)
    mobile_number = db.Column(db.String, index=False, unique=False, nullable=False)
    password_changed_at = db.Column(db.DateTime, index=False, unique=False, nullable=True)
    logged_in_at = db.Column(db.DateTime, nullable=True)
    failed_login_count = db.Column(db.Integer, nullable=False, default=0)
    state = db.Column(db.String, nullable=False, default='pending')

    @property
    def password(self):
        raise AttributeError("Password not readable")

    @password.setter
    def password(self, password):
        self._password = hashpw(password)

    def check_password(self, password):
        return check_hash(password, self._password)


user_to_service = db.Table(
    'user_to_service',
    db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('service_id', db.Integer, db.ForeignKey('services.id'))
)


class Service(db.Model):
    __tablename__ = 'services'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=False,
        default=datetime.datetime.now)
    updated_at = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=True,
        onupdate=datetime.datetime.now)
    active = db.Column(db.Boolean, index=False, unique=False, nullable=False)
    limit = db.Column(db.BigInteger, index=False, unique=False, nullable=False)
    users = db.relationship(
        'User',
        secondary=user_to_service,
        backref=db.backref('user_to_service', lazy='dynamic'))
    restricted = db.Column(db.Boolean, index=False, unique=False, nullable=False)


class ApiKey(db.Model):
    __tablename__ = 'api_key'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    secret = db.Column(db.String(255), unique=True, nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), index=True, nullable=False)
    service = db.relationship('Service', backref=db.backref('api_keys', lazy='dynamic'))
    expiry_date = db.Column(db.DateTime)

    __table_args__ = (
        UniqueConstraint('service_id', 'name', name='uix_service_to_key_name'),
    )


TEMPLATE_TYPES = ['sms', 'email', 'letter']


class Template(db.Model):
    __tablename__ = 'templates'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    template_type = db.Column(db.Enum(*TEMPLATE_TYPES, name='template_type'), nullable=False)
    created_at = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=False,
        default=datetime.datetime.now)
    updated_at = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=True,
        onupdate=datetime.datetime.now)
    content = db.Column(db.Text, index=False, unique=False, nullable=False)
    service_id = db.Column(db.BigInteger, db.ForeignKey('services.id'), index=True, unique=False)
    service = db.relationship('Service', backref=db.backref('templates', lazy='dynamic'))


class Job(db.Model):
    __tablename__ = 'jobs'

    id = db.Column(UUID(as_uuid=True), primary_key=True)
    original_file_name = db.Column(db.String, nullable=False)
    bucket_name = db.Column(db.String, nullable=False)
    file_name = db.Column(db.String, nullable=False)
    service_id = db.Column(db.BigInteger, db.ForeignKey('services.id'), index=True, unique=False)
    service = db.relationship('Service', backref=db.backref('jobs', lazy='dynamic'))
    template_id = db.Column(db.BigInteger, db.ForeignKey('templates.id'), index=True, unique=False)
    template = db.relationship('Template', backref=db.backref('jobs', lazy='dynamic'))
    created_at = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=False,
        default=datetime.datetime.now)
    updated_at = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=True,
        onupdate=datetime.datetime.now)


class VerifyCode(db.Model):
    __tablename__ = 'verify_codes'

    code_types = ['email', 'sms']

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), index=True, nullable=False)
    user = db.relationship('User', backref=db.backref('verify_codes', lazy='dynamic'))
    _code = db.Column(db.String, nullable=False)
    code_type = db.Column(db.Enum(*code_types, name='verify_code_types'), index=False, unique=False, nullable=False)
    expiry_datetime = db.Column(db.DateTime, nullable=False)
    code_used = db.Column(db.Boolean, default=False)
    created_at = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=False,
        default=datetime.datetime.now)

    @property
    def code(self):
        raise AttributeError("Code not readable")

    @code.setter
    def code(self, cde):
        self._code = hashpw(cde)

    def check_code(self, cde):
        return check_hash(cde, self._code)
