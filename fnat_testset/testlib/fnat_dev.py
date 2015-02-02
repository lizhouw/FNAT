from uiautomator import Device
import os


class FnatDevice(Device):
    def __init__(self, serial_no):
        self.serial = serial_no
        Device.__init__(self, serial_no)

