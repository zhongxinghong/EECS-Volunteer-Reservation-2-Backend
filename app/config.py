#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename: config.py
# modified: 2019-10-28

__all__ = [

    "CONFIGS",

    "DevelopmentConfig",
    "TestingConfig",
    "ProductionConfig",

    ]

from .core.const import MYSQL_PROFILE
# from .core.redis.pool import REDIS_CONNECTION_POOL


class BaseConfig(object):

    ENV = "development"
    DEBUG = True
    TESTING = False
    JSON_SORT_KEYS = False
    JSON_AS_ASCII = False

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False

    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{user}:{password}@{host}:{port}/{database}".format(**MYSQL_PROFILE)

    # CACHE_TYPE = "redis"
    # CACHE_OPTIONS = {
    #     "connection_pool": REDIS_CONNECTION_POOL
    # }
    # CACHE_DEFAULT_TIMEOUT = 60 * 5
    # CACHE_KEY_PREFIX = "pkuhelper_v2_api_cache_"

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(BaseConfig):

    ENV = "development"
    DEBUG = True
    TESTING = False
    SQLALCHEMY_ECHO = False


class TestingConfig(BaseConfig):

    ENV = "testing"
    DEBUG = True
    TESTING = True

    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{user}:{password}@{host}:{port}/{database}_test".format(**MYSQL_PROFILE)


class ProductionConfig(BaseConfig):

    ENV = "production"
    DEBUG = False
    TESTING = False


CONFIGS = {

    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,

}