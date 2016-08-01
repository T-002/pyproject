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
"""Tests the service submodule."""
import unittest

from package import service

class ServiceTest(unittest.TestCase):
    """Executes tests for the Service."""

    def test_version(self):
        """Test the version retrieval."""
        version = service.get_version()
        self.assertTrue(version)

    def test_get_sitemap(self):
        """Test the sitemap retrieval."""
        from flask import Flask
        app = Flask(import_name="test_app")
        sitemap = service.get_sitemap(app)

        self.assertTrue(type(sitemap) == list)

    def test_get_sitemap_excludes(self):
        """Test the sitemap retrieval with excludes."""
        from flask import Flask
        app = Flask(import_name="test_app")

        @app.route("/")
        def index():
            return ""       # pragma: no cover

        sitemap = service.get_sitemap(app, [])
        self.assertTrue(len(sitemap) == 2)

        sitemap = service.get_sitemap(app)
        self.assertTrue(len(sitemap) == 0)


