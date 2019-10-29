#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename: user.py
# modified: 2019-10-28

from flask import Blueprint
from ..core.parser import get_str_field
from ..core.wxapi import WxApiClient
from ..models import db, User
from ._wrapper import api_view_wrapper

bpUser = Blueprint("user", __name__)


@bpUser.route("/login", methods=["POST"])
@api_view_wrapper
def login():
    """
    Method   POST
    Form:
        - code    str
    Return:
        - token   char[40]

    """
    code = get_str_field("code")

    wxapi = WxApiClient()
    r = wxapi.auth_code2Session(code)

    openid = r.json()["openid"]

    user = User.get_user_by_openid(openid)

    if user is None:
        user = User(openid)
        with db.session.transaction_start():
            db.session.add(user)

    return {
        "token": user.token,
    }

