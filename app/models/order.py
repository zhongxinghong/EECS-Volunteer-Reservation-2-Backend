#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename: order.py
# modified: 2019-10-29

from ..core.mysql import db
from .order_register import OrderRegister

class Order(db.Model):

    __tablename__ = "order"

    #////////////#
    #   status   #
    #////////////#
    STATUS_WAITING    = 0
    STATUS_PROCESSING = 1
    STATUS_DONE       = 2

    #/////////////#
    # repair type #
    #/////////////#
    REPAIR_TYPE_DUST = "清灰"
    REPAIR_TYPE_SOFTWARE = "软件"
    REPAIR_TYPE_HARDWARE = "硬件"
    REPAIR_TYPE_OTHER = "其它"

    VALID_STATUSES = (STATUS_WAITING, STATUS_PROCESSING, STATUS_DONE)
    VALID_REPAIR_TYPES = (REPAIR_TYPE_DUST, REPAIR_TYPE_SOFTWARE, REPAIR_TYPE_HARDWARE, REPAIR_TYPE_OTHER)

    oid         = db.Column(db.MYSQL_INTEGER, primary_key=True, autoincrement='auto')
    uid         = db.Column(db.MYSQL_VARCHAR(40), db.ForeignKey('user.uid'), nullable=False)
    aid         = db.Column(db.MYSQL_INTEGER, db.ForeignKey('activity.aid'), nullable=False)
    model       = db.Column(db.MYSQL_TEXT, nullable=False)
    description = db.Column(db.MYSQL_TEXT, nullable=False)
    repairType  = db.Column(db.MYSQL_VARCHAR(3), nullable=False)
    period      = db.Column(db.MYSQL_VARCHAR(11), nullable=False)
    email       = db.Column(db.MYSQL_TEXT, nullable=False)
    timestamp   = db.Column(db.MYSQL_BIGINT, nullable=False)
    status      = db.Column(db.MYSQL_TINYINT, nullable=False)

    register    = db.relationship("OrderRegister", backref="order", uselist=False)

    idx_aid     = db.Index("idx_aid", aid)
    idx_uid_aid = db.Index("idx_uid_aid", uid, aid, mysql_prefix="UNIQUE")

    def __init__(self, uid, aid, model, description, repairType, period, email):
        self.uid = uid
        self.aid = aid
        self.model = model
        self.description = description
        self.repairType = repairType
        self.period = period
        self.email = email
        self.status = __class__.STATUS_WAITING
        self.timestamp = self.now()

    @db.validates('repairType')
    def validate_repair_type(self, key, repairType):
        if repairType is None:
            raise AssertionError("repairType is NOT NULL")
        if repairType not in __class__.VALID_REPAIR_TYPES:
            raise AssertionError("invalid repair type %s" % repairType)
        return repairType

    @db.validates('status')
    def validate_status(self, key, status):
        if status is None:
            raise AssertionError("status is NOT NULL")
        if status not in __class__.VALID_STATUSES:
            raise ArithmeticError("invalid status %s" % status)
        return status

    def to_dict(self, excluded=("uid",), with_rid=False):
        res = super().to_dict(excluded=excluded)
        if with_rid:
            register = self.register
            res["rid"] = register.rid if register is not None else None
        return res

    @classmethod
    def get_order_by_oid_aid(cls, oid, aid):
        return cls.query.filter_by(oid=oid, aid=aid).scalar()

    @classmethod
    def get_order_by_uid_aid(cls, uid, aid):
        return cls.query.filter_by(uid=uid, aid=aid).scalar()

    @classmethod
    def list_registered_orders(cls, aid, with_rid=False):
        if not with_rid:
            return cls.query.\
                    join(OrderRegister).\
                    filter(cls.aid == aid).\
                    order_by(cls.status, OrderRegister.rid).\
                    all()
        else:
            return db.session.query(cls, OrderRegister.rid).\
                    join(OrderRegister).\
                    filter(cls.aid == aid).\
                    order_by(cls.status, OrderRegister.rid).\
                    all()

    @classmethod
    def list_orders(cls, aid, with_rid=True):
        if not with_rid:
            return cls.query.\
                    filter(cls.aid == aid).\
                    order_by(db.desc(cls.oid)).\
                    all()
        else:
            return db.session.query(cls, OrderRegister.rid).\
                    outerjoin(OrderRegister).\
                    filter(cls.aid == aid).\
                    order_by(db.desc(cls.oid)).\
                    all()

    @classmethod
    def get_order_counts_of_periods(cls, periods, aid):
        return db.session.query(cls.period, db.func.count(cls.period)).\
                    group_by(cls.period).\
                    filter_by(aid=aid).\
                    all()
