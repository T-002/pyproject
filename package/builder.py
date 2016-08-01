# !/usr/bin/env python
#  -*- coding: UTF-8 -*-

# Copyright (c) 2016 Christian Schwarz
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""This module contains the the main method to build your Flask application."""

import os

from flask import Flask

import service

def make_app(project):
    """Creates a Flask application and returns it.

    :return: Returns a Flask application.
    :rtype:  flask.Flask
    """
    app = Flask(
        import_name     = project,
        static_folder   = "%s/static"    % os.path.dirname(os.path.realpath(__file__)),
        template_folder = "%s/templates" % os.path.dirname(os.path.realpath(__file__)))

    @app.route("/version")
    def get_version():
        """Returns the version of the application."""
        return service.get_version()

    @app.route("/sitemap")
    def get_sitemap():
        """Returns the sitemap of the application."""
        return str(service.get_sitemap(app))

    return app
