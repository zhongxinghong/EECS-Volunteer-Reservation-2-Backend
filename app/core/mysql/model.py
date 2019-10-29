#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename: model.py
# modified: 2019-10-25

__all__ = ["Model"]

import time
from flask_sqlalchemy.model import Model as _Model


class Model(_Model):

    def to_dict(self, excluded=None):
        """
        将查询结果转为 dict
        -------------------
        :Input
            - excluded     None/list/tuple/set   指明要忽略哪些键
        :Warning
            - 部分 model 重载了这个方法

        """
        assert isinstance(excluded, (list, tuple, set, type(None)))

        res = { k:v for k,v in self.__dict__.items() if not k.startswith("_") }

        if excluded is not None:
            return { k:v for k,v in res.items() if k not in excluded }

        return res


    @staticmethod
    def now():
        return int(time.time())
