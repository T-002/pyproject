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

"""This module can be used to adapt the template to your project needs."""

import os

def delete_dummy_files():
    """Delete dummy test files."""
    os.remove("package/dummy.py")
    os.remove("tests/dummy_test.py")

def rename_project(project):
    """Rename the package directory."""
    os.rename("package", project)

def update_test_config(project):
    """Update the test configuration."""
    original = open("tests/__init__.py", "r").read()
    open("tests/__init__.py", "w").write(
        original.replace("package", project))

def update_linter_test(project):
    """Update the linter test."""
    original = open("tests/pylint_test.py", "r").read()
    open("tests/pylint_test.py", "w").write(
        original.replace('PROJECT_NAME="package"', 'PROJECT_NAME="%s"' % project))

def update_noseconfig(project):
    """Update the test configuration to match with the projects package name."""
    original = open("nose.cfg", "r").read()
    open("nose.cfg", "w").write(
        original.replace("cover-package=package,tests", "cover-package=%s,tests" % project))

def update_pylintrc(project):
    """Update the init-hook for pylint."""
    original = open("nose.cfg", "r").read()
    open("nose.cfg", "w").write(original.replace(
        """init-hook='import sys, os; sys.path.insert[0]("."); sys.path.insert[0]("./package");'""",
        """init-hook='import sys, os; sys.path.insert[0]("."); sys.path.insert[0]("./%s");'"""
        % project))

def update_main(project):
    """Remove the not required code from __main__.py"""
    original = open("%s/nose.cfg" % project, "r").read()
    open("nose.cfg", "w").write(
        original.split("####SOME STRING USED TO REMOVE ALL OTHER STUFF")[0])

def main():
    """Run the initializtion and execute all steps to transform the tempalte into a usable project."""
    project = input("Please give your project name: ")

    delete_dummy_files()
    rename_project(project)
    update_test_config(project)
    update_linter_test(project)
    update_noseconfig(project)
    update_pylintrc(project)


if __name__=="__main__":
    main()
