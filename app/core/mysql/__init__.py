#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename: __init__.py
# modified: 2019-10-25

__all__ = ["db"]

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql.types import CHAR, VARCHAR, TEXT, TINYTEXT, INTEGER, TINYINT, BIGINT, MEDIUMTEXT
from .model import Model

db = SQLAlchemy(model_class=Model)


from .utils import transaction_start
db.session.transaction_start = transaction_start  # db.session.begin


db.MYSQL_CHAR = CHAR
db.MYSQL_VARCHAR = VARCHAR
db.MYSQL_TEXT = TEXT
db.MYSQL_TINYTEXT = TINYTEXT
db.MYSQL_MEDIUMTEXT = MEDIUMTEXT
db.MYSQL_INTEGER = INTEGER
db.MYSQL_TINYINT = TINYINT
db.MYSQL_BIGINT = BIGINT
