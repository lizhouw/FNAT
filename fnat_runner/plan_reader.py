#!/usr/bin/env python

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
import adb_obj
import time
import report_server
import gl_var


class plan_reader:
    '''
    This class is to read/process FNAT plan
    '''
    def __init__(self, plan_url):
        self.plan = plan_url
        self.case_list = []
        testset_root = os.environ['FNAT_TESTSET_ROOT']
        os.chdir(testset_root)

    def read_cases(self):
        # Read testplan and extract cases	
        plan_location = "testplan/" + self.plan
        config = ConfigParser.ConfigParser()
        config.read(plan_location)
        all_cases = config.items("cases")
        for case_entry in all_cases:
            left_bracket_pos = case_entry[1].find('(')
            right_bracket_pos = case_entry[1].find(')')
            equal_mark_pos = case_entry[1].rfind('=')
            if (left_bracket_pos >= 0) and (right_bracket_pos > left_bracket_pos + 1) and (equal_mark_pos > right_bracket_pos):
                str_input_param = case_entry[0][left_bracket_pos + 1:right_bracket_pos - 1]
                case_entry = (case_entry[0], case_entry[1][equal_mark_pos + 1:], case_entry[1][left_bracket_pos + 1:right_bracket_pos].strip())
            else:
                case_entry = (case_entry[0], case_entry[1][equal_mark_pos + 1:], "")
                
            if (string.atoi(case_entry[1]) > 0) and (len(case_entry[0].split(".")) > 3):
                # If case iteration is less than or equal to 0, it means that
                # this case is disabled
                # Besides, there must be at least three items in case name, 
                # for, case file name, case class name and case method name
                self.case_list.append(case_entry)

    def set_python_path(self):
        lib_path = os.getcwd() + "/testlib/:" + sys.path[0]
        if os.environ.has_key('PYTHONPATH'):
            os.environ['PYTHONPATH'] = os.environ['PYTHONPATH'] + ":" + lib_path 
        else:
            os.environ['PYTHONPATH'] = lib_path
        
    def run_case(self):
        log_case = None
        sys_stdout = None
        sys_stderr = None

        self.set_python_path()
        try:
            gl_var.adb_mgr = adb_obj.adb_obj()
            gl_var.adb_mgr.restart_adb_server()

            if os.environ.has_key('FNAT_SERIAL_NO'):
                gl_var.adb_mgr.set_adb_serial(os.environ['FNAT_SERIAL_NO'])
            else: 
                gl_var.adb_mgr.get_adb_serial()

            log_folder = os.environ['FNAT_SERIAL_NO']
            log_full_folder = os.environ['FNAT_TESTSET_LOG'] + "/" + log_folder
            if os.path.exists(log_full_folder):
                assert os.path.isdir(log_full_folder)
            else:
                os.makedirs(log_full_folder)

            time.localtime(time.time())
            log_folder += "/Exec-" + time.strftime("%Y-%m-%d-%H-%M-%S")
            log_full_folder = os.environ['FNAT_TESTSET_LOG'] + "/" + log_folder
            os.makedirs(log_full_folder)

            os.environ['FNAT_LOG_FOLDER'] = log_folder

            log_case = open(log_full_folder + "/fnat_case.log", "w+")

            data_server = report_server.report_server()
            exec_id = data_server.create_new_execution()

            for case_entry in self.case_list:
                case_input_params = ""
                if len(case_entry[2]) > 0:
                    input_params = case_entry[2].split(",")
                    for input_param_formular in input_params:
                        param_items = input_param_formular.split("=")
                        case_input_params += " --tc=" + param_items[0].strip()
                        case_input_params += ":" + param_items[1].strip()

                entry_items = case_entry[0].split(".")
                case_cmdline = "testcase/"

                for i in range(0, len(entry_items) - 3):
                    case_cmdline += entry_items[i] + "/"
                case_cmdline += entry_items[-3] + ".py:"
                case_cmdline += entry_items[-2] + "."
                case_cmdline += entry_items[-1]
                print case_cmdline

                exec_loop = string.atoi(case_entry[1])
                for i in range(0, exec_loop):
                    try:
                        if 1 == exec_loop:
                            case_folder = log_full_folder + "/" + case_entry[0]
                        else:
                            case_folder = "%s/%s_%d" % (log_full_folder, case_entry[0], i)
                        os.makedirs(case_folder)

                        if len(case_input_params) > 0:
                            p = subprocess.Popen(["nosetests", "-s", case_input_params, case_cmdline], stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=None)
                        else:
                            p = subprocess.Popen(["nosetests", "-s", case_cmdline], stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=None)
                        r = p.wait()

                        data_server.insert_new_record(exec_id, case_entry[0], r)
                    except Exception as e:
                        print "Exception = ", e
                    finally:
                        # log_buffer = p.stdout.readlines()
                        # for log_line in log_buffer:
                        #    log_case.write(log_line)
                        # log_buffer = p.stderr.readlines()
                        # for log_line in log_buffer:
                        #    log_case.write(log_line)
                        #log_case.flush()
                        adb_cmd = "/system/bin/screencap -p | sed 's/\r$//' > " + case_folder + "/Case_FinalScreen.png"; 
                        gl_var.adb_mgr.run_adb_cmd(adb_cmd)
        finally:
            if None != log_case:
                log_case.close()
