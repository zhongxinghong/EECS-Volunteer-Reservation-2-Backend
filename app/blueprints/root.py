#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename: root.py
# modified: 2019-10-28

import time
from flask import Blueprint
from ..core.parser import get_optional_str_field
from ._wrapper import api_view_wrapper

bpRoot = Blueprint("root", __name__)


@bpRoot.route("/", methods=["GET"])
@api_view_wrapper
def root():
    return {
        "Hello": "World!"
    }


@bpRoot.route("/timestamp", methods=["GET"])
@api_view_wrapper
def timestamp():
    """
    获得系统时间戳

    Method   GET
    Args:
        - unit        str         时间单位，限定 ("ms", "s") 默认 ms
        - format      str         时间变量，限定 ("int", "float") 默认 float
    Return:
        - timestamp   int/float   系统时间

    """
    unit = get_optional_str_field("unit", limited=("ms", "s"), default="ms")
    format_ = get_optional_str_field("format", limited=("int", "float"), default="float")

    t = time.time()
    if unit == "ms":
        t *= 1000
    if format_ == "int":
        t = int(t)

    return {
        "timestamp": t,
    }
