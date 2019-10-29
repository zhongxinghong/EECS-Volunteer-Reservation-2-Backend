#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename: manage.py
# modified: 2019-10-25

import unittest
from werkzeug.serving import run_simple
from flask_script import Manager
from app import create_app, db
from app.models import MODELS


manager = Manager()
manager.app = create_app("development")


@manager.shell
def shell():
    """ Run ipython shell """
    return dict({
        "app": manager.app,
        "db": db,
    }, **MODELS)


@manager.option("-h", "--host", dest="host", default="127.0.0.1")
@manager.option("-p", "--port", dest="port", default=7073)
def runserver(host, port):
    """ Run development server """
    app = manager.app
    run_simple(host, port, app,
               use_reloader=True, use_debugger=True)


@manager.command
def test():
    """ Run unittests """
    tests = unittest.TestLoader().discover("tests/unittests/")
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    manager.run()
