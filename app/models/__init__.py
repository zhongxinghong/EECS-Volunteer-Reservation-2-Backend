#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename: __init__.py
# modified: 2019-10-28

from flask_sqlalchemy.model import DefaultMeta
from ..core.mysql import db
from .user import User
from .admin import Admin
from .activity import Activity
from .order import Order
from .order_register import OrderRegister


_g = globals()

MODELS = {
    k: _g[k]
    for k in [
        var
        for var in dir()
        if not var.startswith("_")
    ]
    if isinstance(_g[k], DefaultMeta)
}
