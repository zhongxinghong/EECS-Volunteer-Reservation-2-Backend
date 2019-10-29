#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename: order_register.py
# modified: 2019-10-28

from ..core.mysql import db

class OrderRegister(db.Model):

    __tablename__ = "order_register"

    rid       = db.Column(db.MYSQL_INTEGER, primary_key=True, autoincrement='auto')
    oid       = db.Column(db.MYSQL_INTEGER, db.ForeignKey('order.oid'), nullable=False)
    timestamp = db.Column(db.MYSQL_BIGINT, nullable=False)

    idx_oid   = db.Index("idx_oid", oid, mysql_prefix="UNIQUE")

    def __init__(self, oid):
        self.oid = oid
        self.timestamp = self.now()
