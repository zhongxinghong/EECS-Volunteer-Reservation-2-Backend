#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename: activity.py
# modified: 2019-10-29

import time
from flask import Blueprint, g
from ..core.parser import get_int_field, get_optional_str_field, get_str_field
from ..core.exceptions import InvalidTimeValue, ActivityNotFound, CannotDeleteActivity
from ..models import db, Activity
from ._wrapper import api_view_wrapper, verify_root_token, verify_user_token

bpActivity = Blueprint("activity", __name__)


def _get_activity_or_raise(aid):
    activity = Activity.query.get(aid)
    if activity is None:
        raise ActivityNotFound
    return activity


def _check_date_and_time(date, begin, end):
    try:
        _ = time.strptime(date, '%Y-%m-%d')
        _ = time.strptime(begin, '%H:%M')
        _ = time.strptime(end, '%H:%M')
    except ValueError:
        raise InvalidTimeValue

    if begin > end:
        raise InvalidTimeValue


@bpActivity.route("/create", methods=["POST"])
@verify_root_token
@api_view_wrapper
def create():
    """
    Method   POST

    Form:
        - date    str   YYYY-mm-dd
        - begin   str   HH-MM
        - end     str   HH-MM
        - site    str

    """
    amid = g.admin.amid

    date = get_str_field("date")
    begin = get_str_field("begin")
    end = get_str_field("end")
    site = get_str_field("site")

    _check_date_and_time(date, begin, end)

    activity = Activity(date, begin, end, site, amid)

    with db.session.transaction_start():
        db.session.add(activity)


@bpActivity.route("/update", methods=["POST"])
@verify_root_token
@api_view_wrapper
def update():
    """
    Method   POST

    Form:
        - aid     int
        - date    str   YYYY-mm-dd
        - begin   str   HH-MM
        - end     str   HH-MM
        - site    str

    """
    amid = g.admin.amid

    aid = get_int_field("aid")
    activity = _get_activity_or_raise(aid)

    date = get_optional_str_field("date", default=activity.date)
    begin = get_optional_str_field("begin", default=activity.begin)
    end = get_optional_str_field("end", default=activity.end)
    site = get_optional_str_field("site", default=activity.site)

    _check_date_and_time(date, begin, end)

    with db.session.transaction_start():
        activity.date = date
        activity.begin = begin
        activity.end = end
        activity.site = site
        activity.amid = amid


@bpActivity.route("/delete", methods=["POST"])
@verify_root_token
@api_view_wrapper
def delete():
    """
    Method   POST

    Form:
        - aid    int

    """
    aid = get_int_field("aid")
    activity = _get_activity_or_raise(aid)

    if activity.orders.count() > 0:
        raise CannotDeleteActivity

    with db.session.transaction_start():
        db.session.delete(activity)  # 可能会因为外键约束而失败


@bpActivity.route("/latest", methods=["GET"])
@verify_user_token
@api_view_wrapper
def latest():
    """
    Method   GET

    Return:
        - activity   dict

    """
    activity = Activity.get_latest_activity()

    return {
        "activity": activity.to_dict()
    }


@bpActivity.route("/list", methods=["GET"])
@verify_root_token
@api_view_wrapper
def list_():
    """
    Method   GET

    Return:
        - activities   list<Activity>
 -
    """
    activities = Activity.list_all()

    return {
        "activities": [ a.to_dict() for a in activities ]
    }
