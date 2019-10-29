#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename: order.py
# modified: 2019-10-29

import datetime
from flask import Blueprint, g
from ..core.parser import get_int_field, get_str_field
from ..core.const import ORDER_PROFILE
from ..core.exceptions import InvalidPeriod, OrderExisted, OrderNotFound, InvalidRegisterToken,\
    CannotWithdrawOrder
from ..models import db, Order, OrderRegister, Activity
from ._wrapper import api_view_wrapper, verify_user_token, verify_admin_token

bpOrder = Blueprint("order", __name__)


_PERIOD_SPAN = ORDER_PROFILE["period_span"]

_periodsCache = {}


def _get_periods(begin, end, span):

    key = (begin, end, span)
    periods = _periodsCache.get(key)
    if periods is not None:
        return periods

    pClock = lambda clockStr: datetime.datetime.strptime(clockStr, "%H:%M")
    fClock = lambda clockObj: datetime.datetime.strftime(clockObj, "%H:%M")

    begin, end = map(pClock, (begin, end))
    span = datetime.timedelta(minutes=span)

    periods = []
    now = begin
    while True:
        if now + span < end:
            periods.append("{}-{}".format(fClock(now), fClock(now + span)))
            now += span
        else:
            periods.append("{}-{}".format(fClock(now), fClock(end)))
            break

    _periodsCache[key] = periods
    return periods


def _is_valid_period(period, activity):
    begin = activity.begin
    end = activity.end
    periods = _get_periods(begin, end, _PERIOD_SPAN)
    return period in periods


def _get_order_or_raise(oid, uid, aid):
    order = Order.get_order_by_uid_aid(uid, aid)
    if order is None or order.oid != oid:
        raise OrderNotFound
    return order


@bpOrder.route("/get_periods", methods=["GET"])
@verify_user_token
@api_view_wrapper
def get_periods():
    """
    Method   GET

    Return:
        - periods   list
        - counts    dict

    """
    activity = Activity.get_latest_activity()

    aid = activity.aid
    begin = activity.begin
    end = activity.end

    periods = _get_periods(begin, end, _PERIOD_SPAN)

    res = Order.get_order_counts_of_periods(periods, aid)
    counts = dict.fromkeys(periods, 0)
    counts.update(dict(res))

    return {
        "periods": periods,
        "counts": counts,
    }


@bpOrder.route("/create", methods=["POST"])
@verify_user_token
@api_view_wrapper
def create():
    """
    Method   POST

    Form:
        - model         str
        - description   str
        - repairType    str
        - period        str
        - email         str

    """
    uid = g.user.uid

    activity = Activity.get_latest_activity()
    aid = activity.aid

    model = get_str_field("model")
    description = get_str_field("description")
    repairType = get_str_field("repairType", limited=Order.VALID_REPAIR_TYPES)
    period = get_str_field("period")
    email = get_str_field("email")

    if not _is_valid_period(period, activity):
        raise InvalidPeriod

    order = Order.get_order_by_uid_aid(uid, aid)
    if order is not None:
        raise OrderExisted

    order = Order(uid, aid, model, description, repairType, period, email)

    with db.session.transaction_start():
        db.session.add(order)


@bpOrder.route("/get_existed", methods=["GET"])
@verify_user_token
@api_view_wrapper
def get_existed():
    """
    Method   GET

    Return:
        - order   dict/None

    """
    uid = g.user.uid

    aid = Activity.get_latest_aid()

    order = Order.get_order_by_uid_aid(uid, aid)

    return {
        "order": order.to_dict(with_rid=True) if order is not None else None
    }


@bpOrder.route("/withdraw", methods=["POST"])
@verify_user_token
@api_view_wrapper
def withdraw():
    """
    Method   POST

    Form:
        - oid   int

    """
    uid = g.user.uid

    oid = get_int_field("oid")

    aid = Activity.get_latest_aid()

    order = _get_order_or_raise(oid, uid, aid)

    if order.register is not None:
        raise CannotWithdrawOrder

    with db.session.transaction_start():
        db.session.delete(order)


@bpOrder.route("/register", methods=["POST"])
@verify_user_token
@api_view_wrapper
def register():
    """
    Method   POST

    Form:
        - oid     int
        - token   char[40]

    """
    uid = g.user.uid

    oid = get_int_field("oid")
    token = get_str_field("token")

    activity = Activity.get_latest_activity()
    aid = activity.aid

    if token != activity.token:
        raise InvalidRegisterToken

    order = _get_order_or_raise(oid, uid, aid)

    register = OrderRegister(oid)

    with db.session.transaction_start():
        db.session.add(register)


@bpOrder.route("/get_register_token", methods=["GET"])
@verify_admin_token
@api_view_wrapper
def get_register_token():
    """
    Method   GET

    Return:
        - token   char[40]

    """
    activity = Activity.get_latest_activity()

    return {
        "token": activity.token
    }


@bpOrder.route("/get_orders", methods=["GET"])
@verify_admin_token
@api_view_wrapper
def get_orders():
    """
    Method   GET

    Return:
        - orders   [Order]

    """
    aid = Activity.get_latest_aid()

    res = Order.list_orders(aid, with_rid=True)

    return {
        "orders": [
            {
                "rid": rid,
                **order.to_dict(),
            }
            for order, rid in res
        ]
    }


@bpOrder.route("/get_queue", methods=["GET"])
@verify_admin_token
@api_view_wrapper
def get_queue():
    """
    Method   GET

    Return:
        - orders   [Order]

    """
    aid = Activity.get_latest_aid()

    res = Order.list_registered_orders(aid, with_rid=True)

    return {
        "orders": [
            {
                "rid": rid,
                **order.to_dict(),
            }
            for order, rid in res
        ]
    }


@bpOrder.route("/change_status", methods=["POST"])
@verify_admin_token
@api_view_wrapper
def change_status():
    """
    Method   POST

    Form:
        - oid      int
        - status   int

    """
    oid = get_int_field("oid")
    status = get_int_field("status", limited=Order.VALID_STATUSES)

    aid = Activity.get_latest_aid()

    order = Order.get_order_by_oid_aid(oid, aid)
    if order is None:
        raise OrderNotFound

    with db.session.transaction_start():
        order.status = status

