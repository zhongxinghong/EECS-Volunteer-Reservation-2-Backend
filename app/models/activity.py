#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename: activity.py
# modified: 2019-10-28

from ..core.mysql import db
from ..core.utils.func import random_string

class Activity(db.Model):

    __tablename__ = "activity"

    aid       = db.Column(db.MYSQL_INTEGER, primary_key=True, autoincrement='auto')
    amid      = db.Column(db.MYSQL_INTEGER, db.ForeignKey('admin.amid'), nullable=False)
    date      = db.Column(db.MYSQL_VARCHAR(10), nullable=False)
    begin     = db.Column(db.MYSQL_VARCHAR(5), nullable=False)
    end       = db.Column(db.MYSQL_VARCHAR(5), nullable=False)
    site      = db.Column(db.MYSQL_TINYTEXT, nullable=False)
    token     = db.Column(db.MYSQL_VARCHAR(40), nullable=False)
    timestamp = db.Column(db.MYSQL_BIGINT, nullable=False)

    orders    = db.relationship("Order", backref="activity", lazy="dynamic")

    idx_token = db.Index("idx_token", token)

    def __init__(self, date, begin, end, site, amid):
        self.date = date
        self.begin = begin
        self.end = end
        self.site = site
        self.amid = amid
        self.token = random_string(40)
        self.timestamp = self.now()

    def to_dict(self, excluded=("amid","token","timestamp")):
        return super().to_dict(excluded=excluded)

    @classmethod
    def get_latest_activity(cls):
        qAid = db.session.query(db.func.max(cls.aid))
        return cls.query.filter(cls.aid == qAid).first()

    @classmethod
    def get_latest_aid(cls):
        return db.session.query(db.func.max(cls.aid)).first()[0]

    @classmethod
    def list_all(cls):
        return cls.query.order_by(db.desc(cls.aid)).all()
