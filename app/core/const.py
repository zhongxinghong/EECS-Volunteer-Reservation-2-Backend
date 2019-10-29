#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename: const.py
# modified: 2019-10-29

__all__ = [

    "EMPTY_DETAIL",

    "PROPERTY_DIR",

    "MYSQL_PROFILE",
    "WXAPI_PROFILE",
    "SAFETY_PROFILE",
    "ORDER_PROFILE",

    ]

import os
from ._internal import load_json_config, abspath


EMPTY_DETAIL = {}

PROPERTY_DIR  = abspath("../../config")


_load_profile = lambda filename: load_json_config(os.path.join(PROPERTY_DIR, filename))

MYSQL_PROFILE  = _load_profile("mysql.json")
WXAPI_PROFILE  = _load_profile("wxapi.json")
SAFETY_PROFILE = _load_profile("safety.json")
ORDER_PROFILE  = _load_profile("order.json")

