#!/usr/bin/python

#
#  File:      run_fnat.py
#  Project:   fnat (Fluke Networks Automation Tester)
#
#  This script is the main entry of project fnat.
#

import os
import sys
import getopt
import plan_reader


def Usage():
    print "run_fnat.py"
    print "  -r, --root: identify root of test set url"
    print "  -p, --plan: identify url of test plan"
    print "  -s, --serial: identify the serial no of device which we want to test"
    print "  -w, --switch: identify the switch we are using, the possible value is in (cisco, hp, huawei)"
    print "  -l, --log:  identify url of execution log"
    print "  -h, --help: print help information"

if __name__ == "__main__":
    try:
        os.unsetenv('FNAT_TESTSET_LOG')
        opts, args = getopt.getopt(sys.argv[1:], 'hp:r:s:w:l:', ['help', 'plan=', 'root=', 'serial=', 'switch=', 'log='])
    except getopt.GetoptError, err:
        print str(err)
        Usage()
        exit(1)

    for o, a in opts:
        if o in ('-h', '--help'):
            Usage()
            exit(0)
        elif o in ('-r', '--root'):
            os.environ['FNAT_TESTSET_ROOT'] = a
        elif o in ('-p', '--plan'):
            plan_testset = a
        elif o in ('-s', '--serial'):
            os.environ['FNAT_SERIAL_NO'] = a
        elif o in ('-w', '--switch'):
            os.environ['FNAT_SWITCH'] = a
        elif o in ('-l', '--log'):
            os.environ['FNAT_TESTSET_LOG'] = a
        else:
            print 'unknown option'
            exit(2)

    print "[FNAT] root = ", os.environ['FNAT_TESTSET_ROOT'], "plan = ", plan_testset
    p_reader = plan_reader.plan_reader(plan_testset)
    p_reader.read_cases()
    p_reader.run_case()
