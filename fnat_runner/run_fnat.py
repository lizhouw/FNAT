#!/usr/bin/python

#
#  File:      run_fnat.py
#  Project:   fnat (Fluke Networks Automation Tester)
#
#  This script is the main entry of project fnat.
#  The syntax is:
#  $ run_fnat.py
#    -r, --root: identify root of test set url
#    -p, --plan: identify url of test plan
#    -l, --log:  identify url of execution log
#    -h, --help: print help information
#

import os
import sys
import getopt
import plan_reader


def Usage():
    print "run_fnat.py"
    print "  -r, --root: identify root of test set url"
    print "  -p, --plan: identify url of test plan"
    print "  -l, --log:  identify url of execution log"
    print "  -h, --help: print help information"

if __name__ == "__main__":
    try:
        os.unsetenv('FNAT_TESTSET_LOG')
        opts, args = getopt.getopt(sys.argv[1:], 'hp:r:l:', ['help', 'plan=', 'root=', 'log='])
    except getopt.GetoptError, err:
        print str(err)
        Usage()
        exit(1)

    for o, a in opts:
        if o in ('-h', '--help'):
            Usage()
            exit(0)
        elif o in ('-r', '--root'):
            root_testset = a
        elif o in ('-p', '--plan'):
            plan_testset = a
        elif o in ('-l', '--log'):
            os.environ['FNAT_TESTSET_LOG'] = a
        else:
            print 'unknown option'
            exit(2)

    try:
        log_case = None
        sys_stdout = None
        sys_stderr = None

        if os.environ.has_key('FNAT_TESTSET_LOG'):
            log_case = open(os.environ['FNAT_TESTSET_LOG'], 'w+')
            sys_stdout = sys.stdout
            sys_stderr = sys.stderr
            sys.stdout = log_case
            sys.stderr = log_case

        print "[FNAT] root = ", root_testset, "plan = ", plan_testset
        os.environ['FNAT_TESTSET_ROOT'] = root_testset
        plan_testset = root_testset + "/testplan/" + plan_testset
        p_reader = plan_reader.plan_reader(plan_testset)
        p_reader.read_cases()
        p_reader.run_case()
    finally:
        if os.environ.has_key('FNAT_TESTSET_LOG'):
            sys.stdout = sys_stdout
            sys.stderr = sys_stderr
            log_case.close()
