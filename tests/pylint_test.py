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

import subprocess
import unittest
import multiprocessing
import os

import jinja2

class ReportGenerator(object):
    """Takes pylint output and creates a readable HTML document."""

    reports = {}

    categories = {
        "R": "Refactor",
        "C": "Convention",
        "W": "Warning",
        "E": "Error",
        "F": "Fatal Error"
    }

    def __init__(self, module_name, pylint_report, output_directory="results/pylint"):
        """Initiates the ReportGenerator.

        :param str  module_name:      Name of the linted module/package.
        :param str  pylint_report:    Linter output.
        :param str  output_directory: Directory to place the reports in.
        """
        super(ReportGenerator, self).__init__()

        self.module_name      = module_name
        self.output_directory = output_directory
        self.pylint_report    = pylint_report
        self.parsed_report    = self.parse_report()

        self.generate_summary()

    @classmethod
    def get_jinja2_template(cls, template_dir="html_templates", template="main.html"):
        """Creates and returns a jinja2.Template.

        :param str template_dir: Directory containing the HTML templates.
        :param str template:     Name of the template.

        :return: Returns the jinja2 environment.
        :rtype:  jinja2.Template
        """
        template_dir = "%s/%s" % (os.path.dirname(os.path.abspath(__file__)), template_dir)
        jinja_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(template_dir),
            trim_blocks=True)

        return jinja_env.get_template(template)

    def generate_summary(self):
        """Generates a summary for the main report."""
        ReportGenerator.reports[self.module_name] = {}

        for category in ["C", "R", "W", "E", "F"]:
            ReportGenerator.reports[self.module_name][category] = 0

            for submodule in self.parsed_report:
                count = len(list(
                    filter(lambda i: i["category"] == category, self.parsed_report[submodule])))

                ReportGenerator.reports[self.module_name][category] += count

        ReportGenerator.reports[self.module_name]["state"] = "ok"

        if ReportGenerator.reports[self.module_name]["C"] > 0:
            ReportGenerator.reports[self.module_name]["state"] = "convention"
        if ReportGenerator.reports[self.module_name]["R"] > 0:
            ReportGenerator.reports[self.module_name]["state"] = "refactor"
        if ReportGenerator.reports[self.module_name]["W"] > 0:
            ReportGenerator.reports[self.module_name]["state"] = "warning"
        if ReportGenerator.reports[self.module_name]["E"] > 0:
            ReportGenerator.reports[self.module_name]["state"] = "error"
        if ReportGenerator.reports[self.module_name]["F"] > 0:
            ReportGenerator.reports[self.module_name]["state"] = "fatal"

    def generate_report_for_submodule(self, module_output):
        """Generates a report for a specific (submodule).

        :param str module_output: pylint output of a specific submodule.
        """
        result = []

        for entry in module_output:
            entry = entry.split(":")

            if len(entry) < 8:
                continue

            result.append({
                "category":      entry[0],
                "category_name": entry[1],
                "message_id":    entry[2],
                "line":          entry[3],
                "column":        entry[4],
                "object":        entry[5],
                "message":       entry[6],
                "symbol":        entry[7]
            })

        result.sort(key=lambda i: i["line"])

        return result

    def parse_report(self):
        """Parses the report into usable format for the ReportGenerator.

        :return: Returns the parsed report.
        :rtype:  list(list)
        """
        result = {}

        for module in self.pylint_report.split("************* Module "):
            module = module.split("\n")
            name = module[0].strip()
            result[module[0]] = self.generate_report_for_submodule(module[1:])

        return result

    def persist_report(self, output_directory):
        """Writes the report to the output_directory.

        :param str output_directory: Directory used to generate the report in.
        """
        template = ReportGenerator.get_jinja2_template(template="module.html")
        outfile = open("%s/%s.html" % (output_directory, self.module_name), "w")
        outfile.write(template.render(
            module_name=self.module_name,
            messages=self.parsed_report))
        outfile.close()

    @classmethod
    def persist_main_report(cls, output_directory):
        """Generated the overview report.

        :param str output_directory: Directory used to generate the report in.
        """
        template = ReportGenerator.get_jinja2_template(template="index.html")
        outfile = open("%s/index.html" % output_directory, "w")
        outfile.write(template.render(reports=cls.reports, categories=ReportGenerator.categories))
        outfile.close()

class PyLintTest(unittest.TestCase):
    """Checks your code with pylint."""

    @classmethod
    def tearDownClass(self):
        """Tears down the PyLintTest class.

        This method will start the overview report generation.
        """
        ReportGenerator.persist_main_report("results/pylint")

    def get_pylint_output_and_status(self, relative_path):
        """Runs pylint on the given path.

        :param str relative_path: Path to the module/package to be checked.

        :return: Returns a tuple containing the output and return code of pylint.
                 Return code 0 means, there were no linter issues.
        :rtype:  tuple(str, int)
        """
        command = "pylint --jobs=%s %s" % (multiprocessing.cpu_count(), relative_path)
        proc = subprocess.Popen(command.split(" "),
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)

        out     = proc.communicate()[0]
        retcode = proc.returncode

        return out.decode("UTF-8"), retcode

    def check_with_pylint_and_generate_report(self, module_name):
        """Checks the given module with pylint and generated the report.

        :param str module_name: Name of the module to be checked.

        :return: Returns the return code of pylint.
        """
        report, retcode = self.get_pylint_output_and_status(module_name)

        # Generate the HTML Report for the module
        rg = ReportGenerator(module_name, report)
        rg.persist_report("results/pylint")

        return retcode

    def test_project(self):
        """Checking the project with pylint."""
        retcode = self.check_with_pylint_and_generate_report("project")
        self.assertEquals(retcode, 0)

    def test_tests(self):
        """Checking your tests with pylint."""
        retcode = self.check_with_pylint_and_generate_report("tests")
        self.assertEquals(retcode, 0)
