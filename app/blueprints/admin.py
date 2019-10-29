#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename: admin.py
# modified: 2019-10-30

from flask import Blueprint
from ..core.parser import get_str_field, get_int_field
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
        - type       int
    Return:
        - token      char[40]

    """
    username = get_str_field("username")
    password = get_str_field("password")
    type = get_int_field("type", limited=Admin.VALID_ADMIN_TYPES)

    admin = Admin.get_admin_by_username_password(username, password, type)

    if admin is None:
        raise Unauthorized

    return {
        "token": admin.token,
    }

