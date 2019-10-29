#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename: internal.py
# modified: 2019-10-29

from flask import Blueprint
from ..core.parser import get_str_field, get_int_field
from ..core.exceptions import Unauthorized
from ..models import db, Admin
from ._wrapper import api_view_wrapper, verify_internal_token

bpInternal = Blueprint("internal", __name__)


@bpInternal.route("/create_admin", methods=["POST"])
@verify_internal_token
@api_view_wrapper
def create_admin():
    """
    Method   POST

    Form:
        - username
        - password
        - type

    """
    username = get_str_field("username")
    password = get_str_field("password")
    type = get_int_field("type", limited=Admin.VALID_ADMIN_TYPES)

    admin = Admin(username, password, type)

    with db.session.transaction_start():
        db.session.add(admin)
