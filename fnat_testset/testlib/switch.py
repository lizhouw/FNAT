#!/usr/bin/python


import ConfigParser
from Cisco import Cisco_dev
from HP import HP_dev
from Huawei import Huawei_dev
import os


class Switch:
    def __init__(self):
        print "Function __init__ of class switch is called"
        env_cfg = os.environ['FNAT_TESTSET_ROOT'] + "/environ.cfg"
        config = ConfigParser.ConfigParser()
        config.read(env_cfg)

        dev_type = os.environ['FNAT_SWITCH'] 
        str_host = config.get(dev_type, "host")
        str_user = config.get(dev_type, "user")
        str_passwd = config.get(dev_type, "passwd")

        if("cisco" == dev_type):
            self.switch_dev = Cisco_dev(str_host, str_user, str_passwd)
        elif("hp" == dev_type):
            self.switch_dev = HP_dev(str_host, str_user, str_passwd)
        elif("huawei" == dev_type):
            self.switch_dev = Huawei_dev(str_host, str_user, str_passwd)
        else:
            assert False

    def set_speed(self, speed):
        print "Function set_speed of class switch is called"
        self.switch_dev.set_speed(speed)
