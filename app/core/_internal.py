#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename: _internal.py
# modified: 2019-10-29

__all__ = [

    "abspath",
    "load_json_config",

    ]

import os
from werkzeug.datastructures import ImmutableDict
from itsdangerous import json


def abspath(*path):
    basedir = os.path.dirname(__file__)
    return os.path.abspath(os.path.join(basedir, *path))

def load_json_config(file):
    assert file.endswith(".json")
    assert os.path.exists(file), "%s profile is missing" % file
    with open(file, "r", encoding="utf-8") as fp:
        data = json.load(fp)
    return ImmutableDict(data)
