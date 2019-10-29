#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename: test_03_activity.py
# modified: 2019-10-28

import unittest
from pprint import pprint
from base import TestCaseMixin
from const import ROOT_USERNAME, ROOT_PASSWORD, WORKER_USERNAME, WORKER_PASSWORD, USER_OPENID
from app.models import Activity

class ActivityTestCase(TestCaseMixin):

    def test_01_create(self):
        activities = [
            {
                # "rid": 1,
                "date": "2019-09-09",
                "begin": "13:30",
                "end": "17:00",
                "site": "理一1127",
            },
            {
                # "rid": 2,
                "date": "2019-10-28",
                "begin": "13:30",
                "end": "17:00",
                "site": "二教105",
            },
            {
                # "rid": 3,
                "date": "2019-11-15",
                "begin": "13:30",
                "end": "17:00",
                "site": "理教207",
            }
        ]

        for activity in activities:
            r = self.post("/activity/create", data=activity, token=self.root_token)
            self.check_status_code(r)
            self.check_errcode(r)
            # pprint([ a.to_dict() for a in Activity.query.all() ])

    def test_02_update(self):
        activity = Activity.get_latest_activity()
        # pprint(activity.to_dict())
        r = self.post("/activity/update", {
                "aid": activity.aid,
                "date": "2019-11-17",
                "site": "二教407",
            }, token=self.root_token)
        self.check_status_code(r)
        self.check_errcode(r)
        # activity = Activity.get_latest_activity()
        # pprint(activity.to_dict())

    def test_03_delete(self):
        activity = Activity.get_latest_activity()
        # pprint([ a.to_dict() for a in Activity.query.all() ])
        r = self.post("/activity/delete", {
                "aid": activity.aid,
            }, token=self.root_token)
        self.check_status_code(r)
        self.check_errcode(r)
        # pprint([ a.to_dict() for a in Activity.query.all() ])

    def test_04_latest(self):
        r = self.get("/activity/latest", token=self.user_token)
        self.check_status_code(r)
        self.check_errcode(r)
        # pprint(r.json)

    def test_05_list(self):
        r = self.get("/activity/list", token=self.root_token)
        self.check_status_code(r)
        self.check_errcode(r)
        # pprint(r.json)

