#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename: client.py
# modified: 2019-10-25

__all__ = ["WxApiClient"]

from requests.sessions import Session
from ..const import WXAPI_PROFILE


_APP_ID = WXAPI_PROFILE["appID"]
_APP_SECRET = WXAPI_PROFILE["appSecret"]

_DEFAULT_TIMEOUT = WXAPI_PROFILE["client"]["default_timeout"]
_USER_AGENT = WXAPI_PROFILE["client"]["user_agent"]


def _get_hooks(*fn):
    return {
        "response": fn,
    }


def _hook_verify_status_code(r, **kwargs):
    if r.status_code != 200:
        r.raise_for_status()


def _hook_verify_error_field(r, **kwargs):
    pass


class WxApiClient(object):

    def __init__(self):
        self._session = Session()
        self._session.headers.update({
            "User-Agent": _USER_AGENT,
        })

    def _request(self, method, url, **kwargs):
        kwargs.setdefault("timeout", _DEFAULT_TIMEOUT)
        return self._session.request(method, url, **kwargs)

    def _get(self, url, params=None, **kwargs):
        return self._request('GET', url, params=params, **kwargs)

    def _post(self, url, data=None, json=None, **kwargs):
        return self._request('POST', url, data=data, json=json, **kwargs)


    def auth_code2Session(self, code):
        r = self._get(
            url="https://api.weixin.qq.com/sns/jscode2session",
            params={
                "appid": _APP_ID,
                "secret": _APP_SECRET,
                "js_code": code,
                "grant_type": "authorization_code",
            },
            hooks=_get_hooks(
                _hook_verify_status_code,
                _hook_verify_error_field,
            ),
        )
        return r

