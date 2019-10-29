#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename: func.py
# modified: 2019-10-28

__all__ = [

    "b",
    "u",

    "base64_encode",
    "base64_decode",
    "urlsafe_base64_encode",
    "urlsafe_base64_decode",

    "random_string",

    ]

import string
import random
import base64


def b(s, encoding="utf-8"):
    """ bytes/str/int/float type to bytes """
    if isinstance(s, bytes):
        return s
    elif isinstance(s, (str, int ,float)):
        return str(s).encode(encoding)
    else:
        raise TypeError(type(s))


def u(s, encoding="utf-8"):
    """ str/int/float/bytes type to utf-8 string """
    if isinstance(s, (str, int, float)):
        return str(s)
    elif isinstance(s, bytes):
        return s.decode(encoding)
    else:
        raise TypeError(type(s))


def base64_encode(s):
    return u(base64.b64encode(b(s)))

def base64_decode(s):
    return base64.b64decode(b(s))

def urlsafe_base64_encode(s):
    return u(base64.urlsafe_b64encode(b(s)))

def urlsafe_base64_decode(s):
    return base64.urlsafe_b64decode(b(s))


def random_string(n, charset=string.ascii_letters+string.digits):
    return ''.join( random.choice(charset) for _ in range(n) )
