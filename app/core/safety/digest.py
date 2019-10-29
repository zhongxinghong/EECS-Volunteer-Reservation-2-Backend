#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename: digest.py
# modified: 2019-10-25

__all__ = [

    "bMD5", "bSHA1", "bSHA256",
    "xMD5", "xSHA1", "xSHA256",

    "bHMAC_MD5", "bHMAC_SHA1", "bHMAC_SHA256",
    "xHMAC_MD5", "xHMAC_SHA1", "xHMAC_SHA256",

    ]

import hashlib
import hmac
from ..utils.func import b, u


def bMD5(s):
    return hashlib.md5(b(s)).digest()

def bSHA1(s):
    return hashlib.sha1(b(s)).digest()

def bSHA256(s):
    return hashlib.sha256(b(s)).digest()

def xMD5(s):
    return hashlib.md5(b(s)).hexdigest()

def xSHA1(s):
    return hashlib.sha1(b(s)).hexdigest()

def xSHA256(s):
    return hashlib.sha256(b(s)).hexdigest()

def bHMAC_MD5(k, s):
    return hmac.new(b(k), b(s), hashlib.md5).digest()

def bHMAC_SHA1(k, s):
    return hmac.new(b(k), b(s), hashlib.sha1).digest()

def bHMAC_SHA256(k, s):
    return hmac.new(b(k), b(s), hashlib.sha256).digest()

def xHMAC_MD5(k, s):
    return hmac.new(b(k), b(s), hashlib.md5).hexdigest()

def xHMAC_SHA1(k, s):
    return hmac.new(b(k), b(s), hashlib.sha1).hexdigest()

def xHMAC_SHA256(k, s):
    return hmac.new(b(k), b(s), hashlib.sha256).hexdigest()