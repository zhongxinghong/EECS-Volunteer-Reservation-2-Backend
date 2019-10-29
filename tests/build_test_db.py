#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename: build_test_db.py
# modified: 2019-10-29

import sys
sys.path.append("../")

from pprint import pprint
from flask import current_app
from requests.sessions import Session
from requests.compat import json

from app import create_app, db
from app.models import Admin, User
from app.core.const import SAFETY_PROFILE
from app.core.exceptions import Success


BASE_URL = "http://127.0.0.1:7073"
APP_CONFIG = "development"
TEST_DATA_JSON = "./test_data.json"
INTERNAL_TOKEN = SAFETY_PROFILE["internal_token"]


ctx = None
data = None
root_token = None
worker_token = None
user_tokens = []


def _hook_check_status_code(r, **kwargs):
    r.raise_for_status()

def _hook_check_errcode(r, **kwargs):
    respJson = r.json()
    if respJson["errcode"] != Success.code:
        raise Exception("[%d] %s" % (respJson["errcode"], respJson["errmsg"]))


class TestClient(object):

    def __init__(self):
        self._session = Session()
        self._session.hooks["response"] = [
            _hook_check_status_code,
            _hook_check_errcode,
        ]

    def _request(self, method, path, **kwargs):
        return self._session.request(method, BASE_URL + path, **kwargs)

    def _get(self, path, params={}, **kwargs):
        return self._request('GET', path, params=params, **kwargs)

    def _post(self, path, data={}, **kwargs):
        return self._request('POST', path, data=data, **kwargs)

    def create_admin(self, username, password, type, internal_token):
        return self._post("/_internal/create_admin", {
                "username": username,
                "password": password,
                "type": type,
            }, headers={
                "Authorization": internal_token
            })

    def create_activity(self, date, begin, end, site, root_token):
        return self._post("/activity/create", {
                "date": date,
                "begin": begin,
                "end": end,
                "site": site,
            }, headers={
                "Authorization": root_token
            })

    def create_order(self, model, description, repairType, period, email, user_token):
        return self._post("/order/create", {
                "model": model,
                "description": description,
                "repairType": repairType,
                "period": period,
                "email": email,
            }, headers={
                "Authorization": user_token
            })

    def get_existed_order(self, user_token):
        return self._get("/order/get_existed", headers={
                "Authorization": user_token,
            })

    def get_register_token(self, admin_token):
        return self._get("/order/get_register_token", headers={
                "Authorization": admin_token,
            })

    def register_order(self, oid, token, user_token):
        return self._post("/order/register", {
                "oid": oid,
                "token": token,
            }, headers={
                "Authorization": user_token
            })


def task_init_app():
    global ctx
    app = create_app(APP_CONFIG)
    ctx = app.app_context()
    ctx.push()


def task_rebuild_db():
    db.drop_all()
    db.create_all()


def task_load_test_data():
    global data
    with open(TEST_DATA_JSON, "r", encoding="utf-8-sig") as fp:
        data = json.load(fp)


def task_create_roots():
    roots = data["roots"]
    client = TestClient()

    for root in roots:
        client.create_admin(
            username=root["username"],
            password=root["password"],
            type=Admin.TYPE_ROOT,
            internal_token=INTERNAL_TOKEN,
        )


def task_get_root_token():
    global root_token
    admin = Admin.query.filter_by(type=Admin.TYPE_ROOT).first()
    root_token = admin.token


def task_create_workers():
    workers = data["workers"]
    client = TestClient()

    for worker in workers:
        client.create_admin(
            username=worker["username"],
            password=worker["password"],
            type=Admin.TYPE_WORKER,
            internal_token=INTERNAL_TOKEN,
        )


def task_get_worker_token():
    global worker_token
    admin = Admin.query.filter_by(type=Admin.TYPE_WORKER).first()
    worker_token = admin.token


def task_create_users():
    users = data["users"]
    client = TestClient()

    with db.session.transaction_start():
        for user in users:
            openid = user["openid"]
            user = User(openid)
            db.session.add(user)


def task_get_user_tokens():
    global user_tokens
    user_tokens = [ u.token for u in User.query.all() ]


def task_create_activities():
    activities = data["activities"]
    client = TestClient()

    for activity in activities:
        client.create_activity(**activity, root_token=root_token)


def task_create_orders():
    orders = data["orders"]
    client = TestClient()

    for idx, order in enumerate(orders):
        client.create_order(**order, user_token=user_tokens[idx])

def task_register_orders():
    orders = data["orders"]
    client = TestClient()

    register_token = client.get_register_token(root_token).json()["detail"]["token"]

    for idx, _ in enumerate(orders):
        user_token = user_tokens[idx]
        order = client.get_existed_order(user_token).json()["detail"]["order"]
        client.register_order(order["oid"], register_token, user_token)



def task_deinit_app():
    ctx.pop()


def main():
    task_init_app()
    task_rebuild_db()
    task_load_test_data()
    task_create_roots()
    task_create_workers()
    task_create_users()
    task_get_root_token()
    task_get_worker_token()
    task_get_user_tokens()
    task_create_activities()
    task_create_orders()
    task_register_orders()
    task_deinit_app()


if __name__ == '__main__':
    main()
