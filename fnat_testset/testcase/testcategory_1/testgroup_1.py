#from uiautomator import Device
from fnat_dev import FnatDevice
import time
import sys
import os


class testclass_1:
    def setUp(self):
        print "Method setUp in class testclass_1"

    def tearDown(self):
        print "Method tearDown in class testclass_1"

    def testmethod_1(self):
        print "Method testmethod_1 in class testclass_1"
        print "PATH = " +  os.environ['PYTHONPATH']
        d = FnatDevice("0c05b1d4dbc84ce8")
        d.press.home()
        time.sleep(0.5)
        d.screenshot("home.png")
        assert True

    def testmethod_2(self):
        print "Method testmethod_2 in class testclass_1"
        assert False

    def testmethod_3(self):
        print "Method testmethod_3 in class testclass_1"

class testclass_2:
    def setUp(self):
        print "Method setUp in class testclass_2"

    def tearDown(self):
        print "Method tearDown in class testclass_2"

    def testmethod_1(self):
        print "Method testmethod_1 in class testclass_2"

    def testmethod_2(self):
        print "Method testmethod_2 in class testclass_2"

    def testmethod_3(self):
        print "Method testmethod_3 in class testclass_2"

