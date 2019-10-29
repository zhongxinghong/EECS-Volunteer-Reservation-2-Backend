#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename: utils.py
# modified: 2019-10-29

__all__ = ["transaction_start"]

from contextlib import contextmanager
from . import db


@contextmanager
def transaction_start():
    try:
        yield
    except Exception:
        db.session.rollback()
        raise
    else:
        db.session.commit()
