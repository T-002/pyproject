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
"""This module contains all API endpoints of the service.

These endpoints are wrapped as functions for reusability.
"""

import sys

def get_version():
    """Returns a readable version of the application.

    :return: Returns the version of the application.
    :rtype:  str
    """
    if sys.version_info >= (3, 0):
        import subprocess
        getoutput = subprocess.getstatusoutput
    else:
        import commands
        getoutput = commands.getstatusoutput

    data = {
        "branch": getoutput("git rev-parse --abbrev-ref HEAD")[1],
        "hash":   getoutput("git rev-parse --short HEAD")[1],
        "date":   datetime.datetime.fromtimestamp(
            int(
                getoutput("git show -s --format=%ct HEAD")[1]
            )).strftime("%Y%m%d.%H%M%S")
    }

    return """v0.%(date)s (%(hash)s-%(branch)s)""" % data

def get_sitemap(app, excludes=["/", "/static/<path:filename>"]):
    """Returns a sitemap for the given application.

    :param flask.Flask app: Application to be scanned.
    :param list excludes:   List of endpoints to be hidden.

    :return: Returns a list containing valid endpoint urls and their methods.
             Example:

                [
                    {"url": "/",         "methods": ["GET"]},
                    {"url": "/username", "methods": ["GET", "POST"]}
                ]

    :rtype:  list
    """
    endpoints = []
    for rule in app.url_map.iter_rules():
        if str(rule) in excludes:
            continue

        endpoint = {}
        endpoint["url"]     = str(rule)
        endpoint["methods"] = ",".join(rule.methods)

        endpoints.append(endpoint)

    endpoints.sort(key= lambda i: i["url"])

    return endpoints
