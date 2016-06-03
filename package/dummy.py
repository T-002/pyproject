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
"""A dummy module, used for testing and demonstration.

This file will be removed during initialization.
"""

class Dummy(object):
    """A dummy class for the project."""

    def __init__(self):
        """Initialized the Dummy."""
        super(Dummy, self).__init__()

        self.call_count = 0

    def add_some_values(self, val_a, val_b):
        """Adds the values a and b.

        :param val_a: First value.
        :param val_b: Second value.

        :return: Returns the addition of a and b.
        """
        self.call_count += 1

        result = val_a + val_b
        return result

    def concatenate_some_values(self, val_a,  val_b):
        """Concatenated the values and returns the result.

        :param val_a: First value.
        :param val_b: Second value.

        :return: Returns the concatenation of val_a and val_b.
        :rtype:  str
        """
        self.call_count += 1

        return "%s%s" % (val_a, val_b)
