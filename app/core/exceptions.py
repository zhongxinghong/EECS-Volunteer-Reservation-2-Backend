#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename: exceptions.py
# modified: 2019-10-29

__all__ = [

"EECSVolunteerReservationException",

    "ServerException",

        "Success",
        "UnknownException",
        "UnderDevelopmentException",
        "DataBaseException",

        "ClientRequestException",
            "FieldKeyMissingError",
            "FieldValueTypeError",
            "LimitedFieldError",
            "FieldValueFormatError",

        "AuthorizationException",
            "Unauthorized",

        "ActivityException",
            "InvalidTimeValue",
            "ActivityNotFound",
            "InvalidPeriod",
            "CannotDeleteActivity",

        "OrderException",
            "OrderExisted",
            "OrderNotFound",
            "InvalidRegisterToken",
            "CannotWithdrawOrder",

]

import traceback
from flask import current_app
from sqlalchemy.exc import SQLAlchemyError, StatementError
from .const import EMPTY_DETAIL


class EECSVolunteerReservationException(Exception):
    """ 项目异常类的抽象基类 """

class ServerException(EECSVolunteerReservationException):
    """ 服务器请求异常的抽象基类 """
    code = None
    desc = ""

    def __init__(self, detail=EMPTY_DETAIL, msg=None):
        cls = self.__class__
        if cls is __class__:
            raise NotImplementedError
        self.detail = detail
        self.msg = msg or cls.desc

    def to_dict(self):
        code = self.__class__.code
        return {
            "errcode": code,
            "errmsg": self.msg,
            "detail": self.detail if (current_app.debug or code == 0) else EMPTY_DETAIL,
        }

    def __repr__(self):
        return str(self.to_dict())

class Success(ServerException):
    """ 无异常 """
    code = 0
    desc = "Success"

class GeneralException(ServerException):
    """ 大类异常 """
    code = -1
    desc = "General Exception"

    def __init__(self, e=None):
        if e is None:
            msg = None
            detail = EMPTY_DETAIL
        elif isinstance(e, Exception):
            msg = "%s.%s: %s" % (e.__class__.__module__, e.__class__.__name__, e)
            detail = {
                "error": repr(e),
                "traceback": traceback.format_exc()
            }
        else:
            msg = str(e)
            detail = {
                "error": str(e)
            }

        super().__init__(detail, msg)

class UnknownException(GeneralException):
    """ 未知异常 """
    code = -1
    desc = "Unknown Exception"

class UnderDevelopmentException(GeneralException):
    """ NotImplementedError 的别名 """
    code = -2
    desc = "Features under development."

class DataBaseException(GeneralException):
    """ 数据库异常 """
    code = -3
    desc = "DataBase Exception"

    # def __init__(self, e=None):
    #     assert isinstance(e, SQLAlchemyError)
    #     if isinstance(e, StatementError): # 不要把 statement / params 的细节放到 msg 里面
    #         msg = "%s.%s: [%s] %s" % (
    #             e.__class__.__module__,
    #             e.__class__.__name__,
    #             e.code,
    #             e.orig,
    #         )
    #         detail = {
    #             "error": repr(e),
    #             "traceback": traceback.format_exc()
    #         }
    #         super(GeneralException, self).__init__(detail, msg)
    #     else:
    #         super().__init__(e)

class ClientRequestException(ServerException):
    """ 客户端请求数据异常 """
    code = 1
    desc = "Client Request Exception"

class FieldKeyMissingError(ClientRequestException):
    """ 缺少某个字段 """
    code = 1001
    desc = "A required field is missing."

class FieldValueTypeError(ClientRequestException):
    """ 字段值类型错误 """
    code = 1002
    desc = "Field type error."

class LimitedFieldError(ClientRequestException):
    """ 字段值超出限制范围 """
    code = 1003
    desc = "Unexpected field value."

class FieldValueFormatError(ClientRequestException):
    """ 字段值值的格式错误 """
    code = 1004
    desc = "Incorrect value format of the field."


class AuthorizationException(ServerException):
    """ 基本鉴权信息错误基类 """
    code = 2
    desc = "Authorization Exception"

class Unauthorized(AuthorizationException):
    """ 鉴权失败 """
    code = 2005
    desc = "Unauthorized"


class ActivityException(ServerException):
    """ 活动相关异常 """
    code = 3
    desc = "Activity Exception"

class InvalidTimeValue(ActivityException):
    """ 日期值无效 """
    code = 3001
    desc = "Invalid time value"

class ActivityNotFound(ActivityException):
    """ 未找到活动 """
    code = 3002
    desc = "Activity not found"

class InvalidPeriod(ActivityException):
    """ 无效的预约时段 """
    code = 3003
    desc = "Invalid period"

class CannotDeleteActivity(ActivityException):
    """ 已经拥有订单的活动不可删除 """
    code = 3004
    desc = "Cannot delete activity"


class OrderException(ServerException):
    """ 订单相关异常 """
    code = 4
    desc = "Order Exception"

class OrderExisted(OrderException):
    """ 当次活动已存在有效订单 """
    code = 4003
    desc = "Order existed"

class OrderNotFound(OrderException):
    """ 未找到订单 """
    code = 4002
    desc = "Order not found"

class InvalidRegisterToken(OrderException):
    """ 无效的挂号凭证 """
    code = 4003
    desc = "Invalid register token"

class CannotWithdrawOrder(OrderException):
    """ 已经挂号的订单不可撤销 """
    code = 4004
    desc = "Cannot withdraw order"
