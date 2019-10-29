#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename: _wrapper.py
# modified: 2019-10-29

__all__ = [

    "api_view_wrapper",

    "verify_internal_token",
    "verify_user_token",
    "verify_admin_token",
    "verify_root_token",
    "verify_worker_token",

    ]

from functools import wraps
from flask import jsonify, g, request
from werkzeug.exceptions import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from ..core.parser import get_optional_str_field
from ..core.const import EMPTY_DETAIL, SAFETY_PROFILE
from ..core.exceptions import Success, EECSVolunteerReservationException, UnknownException,\
    UnderDevelopmentException, DataBaseException, Unauthorized
from ..models import User, Admin


_INTERNAL_TOKEN = SAFETY_PROFILE["internal_token"]


def api_view_wrapper(func):
    """
    API view 函数的外壳
    统一错误捕获和 JSON 响应格式
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            res = func(*args, **kwargs) or EMPTY_DETAIL
        except EECSVolunteerReservationException as e:
            return jsonify(e.to_dict())
        except SQLAlchemyError as e:
            return jsonify(DataBaseException(e).to_dict())
        except HTTPException as e: # abort 404, 405 ...
            raise e
        except NotImplementedError as e:
            return jsonify(UnderDevelopmentException(e).to_dict())
        except Exception as e:
            return jsonify(UnknownException(e).to_dict())
        else:
            return jsonify(Success(res).to_dict())
    return wrapper


def _hook_wrapper(func):
    """
    hook 修饰器内函数的外壳
    统一错误捕获和 JSON 响应格式
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            res = func(*args, **kwargs)
        except EECSVolunteerReservationException as e:
            return jsonify(e.to_dict())
        except SQLAlchemyError as e:
            return jsonify(DataBaseException(e).to_dict())
        except HTTPException as e: # abort 404, 405 ...
            raise e
        except NotImplementedError as e:
            return jsonify(UnderDevelopmentException(e).to_dict())
        except Exception as e:
            return jsonify(UnknownException(e).to_dict())
        else:
            return res
    return wrapper


def _get_token_from_authorization_header():
    token = get_optional_str_field("Authorization", data=request.headers)
    if token is None:
        raise Unauthorized
    return token


def verify_internal_token(func):
    @wraps(func)
    @_hook_wrapper
    def wrapper(*args, **kwargs):

        token = _get_token_from_authorization_header()

        if token != _INTERNAL_TOKEN:
            raise Unauthorized

        g.token = token

        return func(*args, **kwargs)
    return wrapper


def verify_user_token(func):
    @wraps(func)
    @_hook_wrapper
    def wrapper(*args, **kwargs):

        token = _get_token_from_authorization_header()

        user = User.get_user_by_token(token)
        if user is None:
            raise Unauthorized

        g.token = token
        g.user = user

        return func(*args, **kwargs)
    return wrapper


def verify_admin_token(func):
    @wraps(func)
    @_hook_wrapper
    def wrapper(*args, **kwargs):

        token = _get_token_from_authorization_header()

        admin = Admin.get_admin_by_token(token)
        if admin is None:
            raise Unauthorized

        g.token = token
        g.admin = admin

        return func(*args, **kwargs)
    return wrapper


def verify_root_token(func):
    @wraps(func)
    @_hook_wrapper
    def wrapper(*args, **kwargs):

        token = _get_token_from_authorization_header()

        admin = Admin.get_admin_by_token(token, type=Admin.TYPE_ROOT)
        if admin is None:
            raise Unauthorized

        g.token = token
        g.admin = admin

        return func(*args, **kwargs)
    return wrapper


def verify_worker_token(func):
    @wraps(func)
    @_hook_wrapper
    def wrapper(*args, **kwargs):

        token = _get_token_from_authorization_header()

        admin = Admin.get_admin_by_token(token, type=Admin.TYPE_WORKER)
        if admin is None:
            raise Unauthorized

        g.token = token
        g.admin = admin

        return func(*args, **kwargs)
    return wrapper