#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename: test_04_order.py
# modified: 2019-10-29

import unittest
from pprint import pprint
from base import TestCaseMixin
from const import ROOT_USERNAME, ROOT_PASSWORD, WORKER_USERNAME, WORKER_PASSWORD
from app.core.exceptions import OrderExisted, CannotDeleteActivity, CannotWithdrawOrder
from app.models import db, Order, OrderRegister, Activity, User

class OrderTestCase(TestCaseMixin):

    def _get_existed_order(self):
        user = User.get_user_by_token(self.user_token)
        uid = user.uid
        aid = Activity.get_latest_aid()
        return Order.get_order_by_uid_aid(uid, aid)

    def test_01_get_periods(self):
        r = self.get("/order/get_periods", token=self.user_token)
        self.check_status_code(r)
        self.check_errcode(r)
        # pprint(r.json)
        self.periods = r.json["detail"]["periods"]

    def test_02_create(self):

        r = self.get("/order/get_periods", token=self.user_token)
        periods = r.json["detail"]["periods"]

        order = {
            "model": "ThinkPad x230",
            "description": "电脑坏啦哈哈哈 :)",
            "repairType": Order.REPAIR_TYPE_DUST,
            "period": periods[-1],
            "email": "1700012345@pku.edu.cn",
        }

        r = self.post("/order/create", data=order, token=self.user_token)
        self.check_status_code(r)
        self.check_errcode(r)
        # pprint([ o.to_dict() for o in Order.query.all() ])

        r = self.post("/order/create", data=order, token=self.user_token)
        self.check_status_code(r)
        self.check_errcode(r, success=OrderExisted.code)

        aid = Activity.get_latest_aid()
        r = self.post("/activity/delete", {
                "aid": aid,
            }, token=self.root_token)
        self.check_status_code(r)
        self.check_errcode(r, success=CannotDeleteActivity.code)

    def test_03_get_existed(self):
        r = self.get("/order/get_existed", token=self.user_token)
        self.check_status_code(r)
        self.check_errcode(r)
        # pprint(r.json)

    def test_04_withdraw(self):
        order = self._get_existed_order()
        r = self.post("/order/withdraw", {
                "oid": order.oid,
            }, token=self.user_token)
        self.check_status_code(r)
        self.check_errcode(r)
        assert self._get_existed_order() is None
        # pprint([ o.to_dict() for o in Order.query.all() ])
        self.test_02_create()
        # pprint([ o.to_dict() for o in Order.query.all() ])

    def test_05_register(self):
        activity = Activity.get_latest_activity()
        order = self._get_existed_order()

        # r = self.get("/order/get_existed", token=self.user_token)
        # pprint(r.json)
        # r = self.get("/order/get_queue", token=self.worker_token)
        # pprint(r.json)

        r = self.post("/order/register", {
                "oid": order.oid,
                "token": activity.token,
            }, token=self.user_token)
        self.check_status_code(r)
        self.check_errcode(r)
        # pprint([ r.to_dict() for r in OrderRegister.query.all() ])

        # r = self.get("/order/get_existed", token=self.user_token)
        # pprint(r.json)

        r = self.post("/order/withdraw", {
                "oid": order.oid,
            }, token=self.user_token)
        self.check_status_code(r)
        self.check_errcode(r, success=CannotWithdrawOrder.code)

    def test_06_get_register_token(self):
        r = self.get("/order/get_register_token", token=self.worker_token)
        self.check_status_code(r)
        self.check_errcode(r)
        # pprint(r.json)

    def test_07_get_queue(self):
        r = self.get("/order/get_queue", token=self.worker_token)
        self.check_status_code(r)
        self.check_errcode(r)
        # pprint(r.json)

    def test_08_change_status(self):
        r = self.get("/order/get_queue", token=self.worker_token)
        order = r.json["detail"]["orders"][0]
        assert order["status"] == Order.STATUS_WAITING

        r = self.post("/order/change_status", {
                "oid": order["oid"],
                "status": Order.STATUS_PROCESSING,
            }, token=self.worker_token)
        self.check_status_code(r)
        self.check_errcode(r)

        r = self.get("/order/get_queue", token=self.worker_token)
        order = r.json["detail"]["orders"][0]
        assert order["status"] == Order.STATUS_PROCESSING
