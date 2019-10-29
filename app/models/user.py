#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename: user.py
# modified: 2019-10-28

from ..core.mysql import db
from ..core.safety.digest import xSHA1
from ..core.utils.func import random_string
from ..core.const import SAFETY_PROFILE

_USER_OPENID_SALT = SAFETY_PROFILE["user_openid_salt"]


class User(db.Model):

    __tablename__ = "user"

    uid        = db.Column(db.MYSQL_VARCHAR(40), primary_key=True)
    openid     = db.Column(db.MYSQL_VARCHAR(64), nullable=False)
    token      = db.Column(db.MYSQL_VARCHAR(40), nullable=False)

    orders     = db.relationship("Order", backref="user", lazy="dynamic")

    idx_openid = db.Index("idx_openid", openid, mysql_prefix="UNIQUE")
    idx_token  = db.Index("idx_token", token, mysql_prefix="UNIQUE")

    def __init__(self, openid):
        self.uid = __class__.hash_openid(openid)
        self.openid = openid
        self.token = random_string(40)

    @staticmethod
    def hash_openid(openid):
        return xSHA1(openid + _USER_OPENID_SALT)

    @classmethod
    def get_user_by_openid(cls, openid):
        return cls.query.filter_by(openid=openid).scalar()

    @classmethod
    def get_user_by_token(cls, token):
        return cls.query.filter_by(token=token).scalar()
