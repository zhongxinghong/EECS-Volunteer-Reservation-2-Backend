#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename: test_00_begin.py
# modified: 2019-10-29

import unittest
from pprint import pprint
from base import TestCaseMixin
from const import ROOT_USERNAME, ROOT_PASSWORD, WORKER_USERNAME, WORKER_PASSWORD, USER_OPENID
from app.models import db, User, Admin
from app.core.const import SAFETY_PROFILE

class BeginTestCase(TestCaseMixin):

    def test_01_rebuild_db(self):
        uri = self.app.config["SQLALCHEMY_DATABASE_URI"]
        assert uri is not None and uri.endswith("_test")
        self.db.drop_all()
        self.db.create_all()

    def test_02_create_admins(self):
        admins = [
            (ROOT_USERNAME, ROOT_PASSWORD, Admin.TYPE_ROOT),
            (WORKER_USERNAME, WORKER_PASSWORD, Admin.TYPE_WORKER),
        ]
        token = SAFETY_PROFILE["internal_token"]

        for username, password, type in admins:
            r = self.post("/_internal/create_admin", {
                    "username": username,
                    "password": password,
                    "type": type,
                }, token=token)
            self.check_status_code(r)
            self.check_errcode(r)

    def test_03_internal_create_user(self):
        user = User(USER_OPENID)
        with db.session.transaction_start():
            db.session.add(user)
        # pprint(user.token)
        self.user_token = user.token

    def test_04_timestamp(self):
        r = self.get("/timestamp")
        self.check_status_code(r)
        self.check_errcode(r)
        # pprint(r.json)
