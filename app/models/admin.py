#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename: admin.py
# modified: 2019-10-28

from ..core.mysql import db
from ..core.safety.digest import xSHA1
from ..core.utils.func import random_string
from ..core.const import SAFETY_PROFILE

_ADMIN_PASSWORD_SALT = SAFETY_PROFILE["admin_password_salt"]


class Admin(db.Model):

    __tablename__ = "admin"

    #////////////#
    # admin type #
    #////////////#
    TYPE_ROOT = 0
    TYPE_WORKER = 1

    VALID_ADMIN_TYPES = (TYPE_ROOT, TYPE_WORKER)

    amid     = db.Column(db.MYSQL_INTEGER, primary_key=True, autoincrement='auto')
    username = db.Column(db.MYSQL_VARCHAR(64), unique=True, nullable=False)
    password = db.Column(db.MYSQL_VARCHAR(40), nullable=False)
    token    = db.Column(db.MYSQL_VARCHAR(40), unique=True, nullable=False)
    type     = db.Column(db.MYSQL_TINYINT, nullable=False)

    idx_admin = db.Index("idx_admin", username, password)
    idx_token = db.Index("idx_token", token)

    def __init__(self, username, password, type):
        self.username = username
        self.password = self.hash_password(password)
        self.token = random_string(40)
        self.type = type

    @db.validates('type')
    def validate_type(self, key, type):
        if type is None:
            raise AssertionError("type is NOT NULL")
        if type not in __class__.VALID_ADMIN_TYPES:
            raise AssertionError("invalid admin type %s" % type)
        return type

    @staticmethod
    def hash_password(raw):
        return xSHA1(raw + _ADMIN_PASSWORD_SALT)

    @classmethod
    def get_admin_by_username_password(cls, username, password):
        return cls.query.filter_by(username=username, password=cls.hash_password(password)).scalar()

    @classmethod
    def get_admin_by_token(cls, token, type=None):
        if type is not None:
            return cls.query.filter_by(token=token, type=type).scalar()
        else:
            return cls.query.filter_by(token=token).scalar()
