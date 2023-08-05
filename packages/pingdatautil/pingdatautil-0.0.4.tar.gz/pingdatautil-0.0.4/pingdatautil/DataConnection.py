import pyodbc
import jaydebeapi
import os
import sys
import time
from datetime import datetime
import re


class DataConnection():

    def __init__(self, cs=None, mode=None, logger=None):

        if cs:
            self.connection_string = cs
            self.connect()
        else:
            self.connection_string = None

        if mode:
            if mode.lower() in ["odbc", "jdbc"]:
                self.mode = mode.lower()
            else:
                self.mode = "odbc"
        else:
            self.mode = "odbc"

        self.conn = None

        if logger:
            self.logger = logger
        else:
            self.logger = None

        self.ident = "[DATA-CONNECTION]"
        self.separator = "\t"
        self.time = None
        self.time_start = None
        self.time_end = None

    ###############
    ### LOGGING ###
    ##############

    def log(self, input_str, level=None):
        if not self.logger:
            dt_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print("[" + dt_str + "] " + self.ident + " " + input_str)
        else:
            self.logger.log(self.ident + " " + input_str, level)

    def strip_text(self, text):
        text = text.replace("\r", " ").replace("\n", " ").replace("\t", " ").strip()
        return text

    def log_sql(self, input_sql, level=None):
        input_sql = self.strip_text(input_sql)
        self.log("Using SQL Command")
        self.log("=================")
        self.log(input_sql)
        self.log("=================")

    def timer_start(self):
        self.log(F"Timer Start")
        self.time = time.time()

    def timer_stop(self):
        t = time.time()
        i = t - self.time
        txt = "{:.3f}".format(i)
        self.log(F"Finished in {txt}s")
        return txt

    #########################
    ### CONNECTION_STRING ###
    #########################

    def set_connection_string(self, cs, mode=None):
        self.connection_string = cs
        if mode:
            self.set_mode(mode)

    def set_cs(self, cs, mode=None):
        self.set_connection_string(cs, mode)

    def set_mode(self, mode):
        if mode.lower() in ["odbc", "jdbc"]:
            self.mode = mode.lower()
        else:
            self.mode = "odbc"

    def connect(self, cs=None, mode=None):

        if cs:
            self.set_connection_string(cs, mode)

        if self.mode == "odbc":
            if isinstance(self.connection_string, str):
                try:
                    self.conn = pyodbc.connect(self.connection_string)
                    self.log("Connect to database successfully.")
                except Exception as e:
                    self.log("Cannot connect to database", "ERROR")
                    self.log(str(e), "ERROR")
                    sys.exit(-1)
            else:
                self.log("ODBC mode must set connection string as odbc string", "ERROR")
                sys.exit(-1)

        elif self.mode == "jdbc":

            if isinstance(self.connection_string, dict):
                try:
                    dict_cstr = self.connection_string
                    self.conn = jaydebeapi.connect(dict_cstr["class"], dict_cstr["jdbc"],
                                                   [dict_cstr["user"], dict_cstr["pass"]], dict_cstr["driver"])
                    self.log("Connect to database successfully.")
                except Exception as e:
                    self.log("Cannot connect to database", "ERROR")
                    self.log(str(e), "ERROR")
                    sys.exit(-1)
            else:
                self.log("JDBC mode must set connection string as dictionary", "ERROR")
                sys.exit(-1)

    def close(self):
        self.conn.close()

    #########################
    ### HELPER FUNCTION ###
    #########################

    def count_records(self, sql_command):
        self.log(f"Count records using: {sql_command}")
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql_command)
            row = cursor.fetchone()
            cnt = row[0]
            cnt_str = '{:,}'.format(cnt)
            cursor.close()
            self.log(f"Records count: {str(cnt_str)}")
        except Exception as e:
            cnt = None
            self.log(f"str(e)", "ERROR")
        return cnt

    def execute(self, sql_command):
        sql_txt = sql_command.replace("\r", " ").replace("\n", " ").replace("\t", " ").strip()
        self.log(F"Using: {sql_txt}")
        self.timer_start()
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql_command)
            cursor.commit()
            cursor.close()
        except Exception as e:
            self.log(F"{str(e)}", "ERROR")
            cursor.rollback()
            cursor.close()
        txt = self.timer_stop()
        return txt

    def execute_fetch(self, sql_command, rows=None):
        self.log_sql(sql_command)
        self.timer_start()
        if not rows:
            rows = 1
        self.log(f"Fetch first {str(rows)} row(s).")
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql_command)
            list_rows = cursor.fetchmany(rows)
            for i, row in enumerate(list_rows):
                self.log(F"#{str(i + 1)} : {str(row)}")
            cursor.close()
        except Exception as e:
            self.log(F"{str(e)}", "ERROR")
            cursor.close()
        txt = self.timer_stop()
        return txt

    def execute_full(self, sql_command, with_result=None):
        self.log_sql(sql_command)
        self.timer_start()
        r = 0
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql_command)
            if with_result:
                row = cursor.fetchone()
                self.log("Sample Data")
                r = row[0]
                self.log(F"{str(row)}")
            cursor.close()
        except Exception as e:
            self.log(F"{str(e)}", "ERROR")
            cursor.close()
        txt = self.timer_stop()
        return txt
