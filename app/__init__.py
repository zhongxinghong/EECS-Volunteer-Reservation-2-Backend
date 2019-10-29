#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename: __init__.py
# modified: 2019-10-28

__all__ = ["create_app"]

from flask import Flask
from .config import CONFIGS, DevelopmentConfig
from .blueprints import bpRoot, bpInternal, bpUser, bpAdmin, bpActivity, bpOrder
from .core.mysql import db


def create_app(config):

    app = Flask(__name__)

    _Config = CONFIGS[config]
    app.config.from_object(_Config)

    db.init_app(app)

    app.register_blueprint(bpRoot)
    app.register_blueprint(bpInternal, url_prefix="/_internal")
    app.register_blueprint(bpUser, url_prefix="/user")
    app.register_blueprint(bpAdmin, url_prefix="/admin")
    app.register_blueprint(bpActivity, url_prefix="/activity")
    app.register_blueprint(bpOrder, url_prefix="/order")

    return app
