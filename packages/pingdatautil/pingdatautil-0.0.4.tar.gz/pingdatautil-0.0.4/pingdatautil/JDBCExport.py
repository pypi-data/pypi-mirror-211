import jaydebeapi as jdbc
import pandas as pd
import os, sys
import csv
import codecs
import sys
import time
from datetime import datetime
import warnings

warnings.filterwarnings("ignore", category=UserWarning)


class JDBCExport():

    def __init__(self, dict_cs=None, logger=None):
        if dict_cs:
            self.connection_string = dict_cs
            self.connect()
        else:
            self.connection_string = None

        self.dialect = "MSSQL"
        self.separator = "\t"
        self.conn = None
        self.time = None
        self.time_start = None
        self.time_end = None
        self.total_record = 0
        self.total_time = 0
        self.break_row_count = 5000
        self.multiply_varchar = 1
        self.varchar_max = 4000
        self.show_header = True
        self.cols = None
        self.verbose = False
        self.need_clean = True
        self.with_data_date_column = None
        self.default_name = "EXPORT"

        if logger:
            self.logger = logger
        else:
            self.logger = None

    ###############
    ### LOGGING ###
    ##############

    def log(self, input_str, level=None):
        ident = "[JDBC-EXPORT]"
        if not self.logger:
            dt_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print("[" + dt_str + "] " + ident + " " + input_str)
        else:
            self.logger.log(ident + " " + input_str, level)

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

    def set_connection_string(self, cs):
        self.connection_string = cs

    def set_cs(self, cs):
        self.connection_string = cs

    def connect(self, dict_cs=None):
        if dict_cs:
            self.connection_string = dict_cs
        try:
            dict_cstr = self.connection_string
            self.conn = jdbc.connect(dict_cstr["class"], dict_cstr["jdbc"],
                                     [dict_cstr["user"], dict_cstr["pass"]], dict_cstr["driver"])
            self.log("Connect to database successfully.")
        except Exception as e:
            self.log("Cannot connect to database", "ERROR")
            self.log(str(e), "ERROR")
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

    def execute_full(self, sql_command, with_result=None):
        sql_txt = sql_command.replace("\r", " ").replace("\n", " ").replace("\t", " ").strip()
        self.log(F"Using: {sql_txt}")
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

    def query(self, query_str):
        df = pd.read_sql_query(query_str, self.conn)
        print(df)

    #########################
    ### ODBC UTIL FUNCTION ###
    #########################

    def get_col_name_list(self, cursor):
        col_name = [column[0] for column in cursor.description]
        if self.with_data_date_column:
            col_name.append(self.with_data_date_column)
        return col_name

    def get_col_metadata(self, cursor):
        cols = [[column[0], str(column[1]).replace("<class '", "").replace("'>", ""), column[4], column[5]] for column
                in
                cursor.description]
        if self.with_data_date_column:
            cols.append([self.with_data_date_column, 'datetime.datetime', None, None])
        return cols

    def get_cursor_definition(self, sql_command):
        self.log("Starting Query")
        self.timer_start()
        cursor = self.conn.cursor()
        cursor.execute(sql_command)
        self.log("Using SQL Command : ")
        self.log("--=============================--")
        self.log("\n" + sql_command)
        self.log("--=============================--")
        col_metadata = self.get_col_metadata(cursor)
        self.cols = col_metadata
        self.log(col_metadata)
        cursor.close()
        self.timer_stop()
        return col_metadata

    #########################
    ### MAIN FUNCTION ###
    #########################

    def export_query_to_text(self, sql_command, text_file, separator=None):

        sql_txt = sql_command.replace("\r", " ").replace("\n", " ").replace("\t", " ").strip()
        # Time
        self.log("Starting Export")
        self.timer_start()
        # data_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        data_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Start
        cursor = self.conn.cursor()
        cursor.execute(sql_command)
        self.log("Using SQL Command : ")
        self.log("--=============================--")
        self.log(sql_txt)
        self.log("--=============================--")
        # print(cursor.description)
        col_name = self.get_col_name_list(cursor)
        col_metadata = self.get_col_metadata(cursor)
        self.cols = col_metadata

        list_string_column = []
        for i, col in enumerate(col_metadata):
            if col[1] == "str":
                list_string_column.append(i)

        if separator:
            separator = separator
        else:
            separator = self.separator

        self.log(f"Separator is : {separator}")

        f = codecs.open(text_file, mode="w+", encoding="utf-8")
        header_string = separator.join(col_name)
        header_string_csv = ",".join(col_name)
        if self.verbose or self.show_header:
            self.log("List header columns : " + header_string_csv)
        f.write(header_string + "\r\n")
        rec = 0

        row = cursor.fetchone()
        while row is not None:
            rec += 1

            # CLEAN_ROW
            if self.need_clean:
                for j, r in enumerate(row):
                    if j in list_string_column:
                        if row[j]:
                            row[j] = row[j].strip().replace("\t", "").replace("\n", "").replace("\r", "")

            if rec % self.break_row_count == 0:
                self.log("{rec} records passed.".format(rec=str(rec)))
            if self.verbose:
                # self.testrow = row
                # print(row)
                print(*row, sep=separator)

            if self.with_data_date_column:
                csv.writer(f, quoting=csv.QUOTE_NONE, escapechar='\\', delimiter=separator).writerow(
                    list(row) + [data_date])
            else:
                csv.writer(f, quoting=csv.QUOTE_NONE, escapechar='\\', delimiter=separator).writerow(row)

            row = cursor.fetchone()

        self.total_record = rec
        self.log("Total {rec} records.".format(rec=str(rec)))
        self.log("Finished export to {file}".format(file=text_file))

        # Time
        self.timer_stop()
        f.close()
        cursor.close()
