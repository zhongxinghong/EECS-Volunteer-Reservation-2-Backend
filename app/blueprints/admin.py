#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename: admin.py
# modified: 2019-10-28

from flask import Blueprint
from ..core.parser import get_str_field
from ..core.exceptions import Unauthorized
from ..models import db, Admin
from ._wrapper import api_view_wrapper

bpAdmin = Blueprint("admin", __name__)


@bpAdmin.route("/login", methods=["POST"])
@api_view_wrapper
def login():
    """
    Method   POST

    Form:
        - username   str
        - password   str
    Return:
        - token      char[40]

    """
    username = get_str_field("username")
    password = get_str_field("password")

    admin = Admin.get_admin_by_username_password(username, password)

    if admin is None:
        raise Unauthorized

    return {
        "token": admin.token,
    }

