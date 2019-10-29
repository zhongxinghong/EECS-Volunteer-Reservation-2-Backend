#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename: parser.py
# modified: 2019-10-28

__all__ = [

    "get_field",

    "get_str_field",
    "get_optional_str_field",
    "get_int_field",
    "get_optional_int_field",
    "get_float_field",
    "get_optional_float_field",
    "get_boolean_field",
    "get_optional_boolean_field",

    ]

from flask import request
from werkzeug.datastructures import Headers
from .exceptions import FieldKeyMissingError, FieldValueTypeError, LimitedFieldError, FieldValueFormatError


_TRUE_VALUES  = ( "1", "true" )
_FALSE_VALUES = ( "0", "false" )

def _bool(s):
    """ string->bool """
    s = s.lower()
    if s in _TRUE_VALUES:
        return True
    if s in _FALSE_VALUES:
        return False
    raise ValueError


def get_field(type_, key, limited=None, regex=None, data=None, nullable=False, default=None):
    """
    用于表单值解析的函数模板
    用于解析表单值，并校验其合理性
    ----------------------------
    Input
        - key         str/tupel/list/set    表单 key 可以传入多个，标识键名有多种可能
        - limited     tuple/list/set        表单 value 的合理值范围
        - regex       re.compile            编译好的正则表达式实例，用于检查 value 的格式
        - data        dict                  指定解析的数据源，否则根据 request.method 判断数据源
        - nullable    bool                  若设为 True ，则当 key 不存在于表单中时，会返回 None
        - default     object                如果 nullable 则返回这个默认值

    """
    assert isinstance(data, (dict, Headers, type(None))), type(data)
    assert isinstance(limited, (tuple, list, set, type(None))), type(limited)

    if data is not None:
        _data = data
    elif request.method == "GET":
        _data = request.args
    elif request.is_json:
        _data = request.json
    elif request.method == "POST":
        _data = request.form
    else:
        _data = request.values()

    if isinstance(key, str):
        value = _data.get(key)
    elif isinstance(key, (tuple, list, set)):
        for k in key:
            if k in _data:
                value = _data[k]
                break
        else:
            value = None
    else:
        raise TypeError(type(key)) # 内部错误

    if value is None:
        if nullable:
            return default # default 默认值为 None
        elif isinstance(key, str):
            raise FieldKeyMissingError
        elif isinstance(key, (tuple, list, set)):
            raise FieldKeyMissingError
        else:
            raise TypeError(type(key)) # 内部错误

    try:
        value = type_(value)
    except ValueError:
        if value == '' and nullable:
            return None
        else:
            raise FieldValueTypeError

    if limited is not None and value not in limited:
        raise LimitedFieldError

    if regex is not None and regex.match(value) is None:
        raise FieldValueFormatError

    return value


def get_str_field(key, limited=None, regex=None, data=None):
    return get_field(str, key, limited=limited, regex=regex, data=data, nullable=False)

def get_optional_str_field(key, limited=None, regex=None, data=None, default=None):
    return get_field(str, key, limited=limited, regex=regex, data=data, nullable=True, default=default)

def get_int_field(key, limited=None, data=None):
    return get_field(int, key, limited=limited, data=data, nullable=False)

def get_optional_int_field(key, limited=None, data=None, default=None):
    return get_field(int, key, limited=limited, data=data, nullable=True, default=default)

def get_float_field(key, limited=None, data=None):
    return get_field(float, key, limited=limited, data=data, nullable=False)

def get_optional_float_field(key, limited=None, data=None, default=None):
    return get_field(float, key, limited=limited, data=data, nullable=True, default=default)

def get_boolean_field(key, data=None):
    return get_field(_bool, key, data=data, nullable=False)

def get_optional_boolean_field(key, data=None, default=None):
    return get_field(_bool, key, data=data, nullable=True, default=default)
