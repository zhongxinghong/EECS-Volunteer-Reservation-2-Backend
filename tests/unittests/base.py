#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename: base.py
# modified: 2019-10-28

import time
import unittest
from pprint import pprint
from flask import current_app
from flask.testing import FlaskClient
from cache import CacheMixin
from app import create_app, db
from app.core.exceptions import Success


class TestCaseMixin(unittest.TestCase, CacheMixin):

    def setUp(self):
        self.app = create_app("testing")
        self.ctx = self.app.app_context()
        self.ctx.push()
        self.client = current_app.test_client()
        self.db = db

    def tearDown(self):
        self.ctx.pop()

    def _with_auth_header(self, kwargs, token=None):
        if token is not None:
            kwargs["headers"] = {
                "Authorization": token
            }
        return kwargs

    def get(self, path, params={}, token=None):
        kwargs = {
            "query_string": params
        }
        self._with_auth_header(kwargs, token=token)
        return self.client.get(path, **kwargs)

    def post(self, path, data={}, token=None):
        kwargs = {
            "data": data
        }
        self._with_auth_header(kwargs, token=token)
        return self.client.post(path, **kwargs)

    def check_status_code(self, r, code=200):
        statusCode = r.status_code
        try:
            self.assertTrue(statusCode == code, statusCode)
        except AssertionError as e:
            pprint(r.json)
            raise e

    def check_errcode(self, r, success=Success.code):
        errcode = r.json["errcode"]
        try:
            self.assertTrue(errcode == success, errcode)
        except AssertionError as e:
            pprint(r.json)
            raise e

