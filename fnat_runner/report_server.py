import ConfigParser
import MySQLdb
import os
import string
import adb_obj
import gl_var


class report_server:
    def __init__(self):
        try:
            env_cfg = os.environ['FNAT_TESTSET_ROOT'] + "/environ.cfg"
            config = ConfigParser.ConfigParser()
            config.read(env_cfg)

            str_host = config.get("ReportServer", "host")
            str_user = config.get("ReportServer", "user")
            str_passwd = config.get("ReportServer", "passwd")
            str_port = config.get("ReportServer", "port")

            self.conn = MySQLdb.connect(host = str_host, user = str_user, passwd = str_passwd, port = string.atoi(str_port))
            self.conn.select_db("fnat_base")
        except Exception as e:
            print "Exception = ", e

    def create_new_execution(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("BEGIN")

            list_build = gl_var.adb_mgr.run_adb_cmd("getprop ro.build.display.id")
            if 1 != len(list_build):
                assert False
            str_build = list_build[0].strip()

            sql_cmd = "INSERT INTO fnat_execution(build_number, start_time, serial_no, log_location) VALUES(";
            sql_cmd += "'" + str_build + "', ";
            sql_cmd += "now(), "
            sql_cmd += "'" + os.environ['FNAT_SERIAL_NO'] + "', "
            sql_cmd += "'" + os.environ['FNAT_LOG_FOLDER'] + "')"
            print "sql_cmd = ", sql_cmd
            cursor.execute(sql_cmd)

            count = cursor.execute("SELECT @@IDENTITY")
            assert (1 == count)

            exec_id = cursor.fetchone()[0]
            cursor.execute("COMMIT")

            return exec_id
        except Exception as e:
            print "Exception = ", e

