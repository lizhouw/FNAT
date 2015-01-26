#!/usr/bin/python

#
#  File:      plan_reader.py
#  Project:   fnat (Fluke Networks Automation Tester)
#
#  This script is used in project fnat to write/parse test plan.
#

import ConfigParser
import os
import string
import subprocess
import sys


class plan_reader:
    '''
    This class is to read/process FNAT plan
    '''
    def __init__(self, plan_url):
        self.plan = plan_url
        self.case_list = []

    def read_cases(self):
        config = ConfigParser.ConfigParser()
        config.read(self.plan)
        all_cases = config.items("cases")
        for case_entry in all_cases:
            if (string.atoi(case_entry[1]) > 0) and (len(case_entry[0].split(".")) > 3):
                # If case iteration is less than or equal to 0, it means that
                # this case is disabled
                # Besides, there must be at least three items in case name, 
                # for, case file name, case class name and case method name
                self.case_list.append(case_entry)

    def run_case(self):
        case_location = os.environ['FNAT_TESTSET_ROOT'] + "/testcase"
        os.chdir(case_location)

        for case_entry in self.case_list:
            entry_items = case_entry[0].split(".")
            case_cmdline = ""

            for i in range(0, len(entry_items) - 3):
                case_cmdline += entry_items[i] + "/"
            case_cmdline += entry_items[-3] + ".py:"
            case_cmdline += entry_items[-2] + "."
            case_cmdline += entry_items[-1]


            for i in range(0, string.atoi(case_entry[1])):
                p = subprocess.Popen(["nosetests", "-s", case_cmdline], stdout=sys.stdout, stderr=sys.stderr)
                p.wait()
