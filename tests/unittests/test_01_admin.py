#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename: test_01_admin.py
# modified: 2019-10-30

import unittest
from pprint import pprint
from base import TestCaseMixin
from const import ROOT_USERNAME, ROOT_PASSWORD, WORKER_USERNAME, WORKER_PASSWORD
from app.models import Admin

class AdminTestCase(TestCaseMixin):

    def test_01_login_admins(self):
        admins = [
            (ROOT_USERNAME, ROOT_PASSWORD, "root_token", Admin.TYPE_ROOT),
            (WORKER_USERNAME, WORKER_PASSWORD, "worker_token", Admin.TYPE_WORKER),
        ]

        for username, password, key, type in admins:
            r = self.post("/admin/login", {
                    "username": username,
                    "password": password,
                    "type": type,
                })
            self.check_status_code(r)
            self.check_errcode(r)
            # pprint(r.json)
            setattr(self, key, r.json["detail"]["token"])
