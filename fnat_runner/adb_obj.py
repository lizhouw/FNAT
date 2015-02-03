import os


class adb_obj:
    def __init__(self):
        pass

    def start_adb_server(self):
        this_cmd = "adb start-server"
        os.system(this_cmd)

    def kill_adb_server(self):
        this_cmd = "adb kill-server"
        os.system(this_cmd)

    def restart_adb_server(self):
        self.kill_adb_server()
        self.start_adb_server()

    def adb_push_file(self, src_path, dst_path):
        this_cmd = "adb -s " + self.serial + " push " + src_path + " " + dst_path
        return os.popen(this_cmd).readlines()

    def adb_pull_file(self, src_path, dst_path):
        this_cmd = "adb -s " + self.serial + " pull " + src_path + " " + dst_path
        return os.popen(this_cmd).readlines()

    def set_adb_serial(self, serial_no):
        self.serial = serial_no

    def get_adb_serial(self):
        this_cmd = "adb devices"
        cmd_output = os.popen(this_cmd).readlines()
        if (3 == len(cmd_output)) and (0 == cmd_output[0].find("List of devices attached")):
            this_line = cmd_output[1].split()
            if (2 == len(this_line)) and ("device" == this_line[1]):
                os.environ['FNAT_SERIAL_NO'] = this_line[0]
                self.serial = os.environ['FNAT_SERIAL_NO']
            else:
                assert False
        else:
            assert False

    def run_adb_cmd(self, adb_cmd):
        this_cmd = "adb -s " + self.serial + " shell  " + adb_cmd
        return os.popen(this_cmd).readlines()

