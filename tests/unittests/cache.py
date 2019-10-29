#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename: cache.py
# modified: 2019-10-29

class CacheMixin(object):

    _cache = {}

    @property
    def root_token(self):
        return self._cache["root_token"]

    @root_token.setter
    def root_token(self, value):
        self._cache["root_token"] = value

    @property
    def worker_token(self):
        return self._cache["worker_token"]

    @worker_token.setter
    def worker_token(self, value):
        self._cache["worker_token"] = value

    @property
    def user_token(self):
        return self._cache["user_token"]

    @user_token.setter
    def user_token(self, value):
        self._cache["user_token"] = value

