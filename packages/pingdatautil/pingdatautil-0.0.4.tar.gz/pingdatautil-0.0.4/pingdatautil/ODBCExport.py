import codecs
import shutil
import gzip
import csv
import os
import pyodbc
import sys
import time
import zipfile
from datetime import datetime
import pandas as pd
import re


class ODBCExport():

    def __init__(self, cs=None, logger=None):
        if cs:
            self.connection_string = cs
            self.connect()
        else:
            self.connection_string = None
        self.dialect = "MSSQL"
        self.separator = "\t"
        self.conn = None
        self.show_header = True
        self.show_table_command = None
        self.table_command = None
        self.cols = None
        self.verbose = False
        self.need_clean = True
        self.total_record = 0
        self.time = None
        self.time_start = None
        self.time_end = None
        self.total_time = 0
        self.with_data_date_column = None
        self.default_name = "EXPORT"
        self.break_row_count = 5000
        self.multiply_varchar = 1
        self.varchar_max = 4000
        self.prefer_bigint = False

        if logger:
            self.logger = logger
        else:
            self.logger = None

    ###############
    ### LOGGING ###
    ##############

    def log(self, input_str, level=None):
        ident = "[ODBC-EXPORT]"
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

    def connect(self, cs=None):
        if cs:
            self.connection_string = cs
        try:
            self.conn = pyodbc.connect(self.connection_string)
            self.log("Connect to database successfully.")
        except Exception as e:
            self.log("Cannot connect to database", "ERROR")
            self.log(str(e), "ERROR")
            sys.exit(-1)

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

    def close(self):
        self.conn.close()


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

    def get_create_table_command(self):
        table_str = "DROP TABLE " + self.default_name + ";\n"
        table_str += "CREATE TABLE " + self.default_name + " (\n"
        cols = self.cols
        self.log(F"ODBC Column Description : {str(cols)}")

        trail = ","
        for i, c in enumerate(cols):
            if i == len(cols) - 1:
                trail = ""

            col_string = c[1].upper()
            if self.dialect == "MSSQL":
                if col_string == "STR":
                    c_len = c[2] * self.multiply_varchar
                    if c_len >= self.varchar_max:
                        c_len = self.varchar_max
                    else:
                        pass
                    col_string = "NVARCHAR({len})".format(len=str(c_len))
                elif col_string == "DATETIME.DATETIME":
                    col_string = "DATETIME"
                elif col_string == "DATETIME.DATE":
                    col_string = "DATE"
                elif col_string == "DECIMAL.DECIMAL":
                    col_string = "DECIMAL({d},{p})".format(d=str(c[2]), p=str(c[3]))
                elif col_string == "INT":
                    c_len = c[2]
                    if c_len > 8:
                        col_string = "BIGINT"
                    else:
                        col_string = "INT"

            if self.dialect == "PG":
                if col_string == "STR":
                    c_len = c[2] * self.multiply_varchar
                    if c_len >= self.varchar_max:
                        c_len = self.varchar_max
                    else:
                        pass
                    col_string = "VARCHAR({len})".format(len=str(c_len))
                elif col_string == "DATETIME.DATETIME":
                    col_string = "TIMESTAMP"
                elif col_string == "DATETIME.DATE":
                    col_string = "DATE"
                elif col_string == "DECIMAL.DECIMAL":
                    col_string = "NUMERIC({d},{p})".format(d=str(c[2]), p=str(c[3]))
                elif col_string == "INT":
                    c_len = c[2]
                    if c_len > 8:
                        col_string = "BIGINT"
                    else:
                        col_string = "INT"
            else:
                pass

            table_str += "\t" + c[0] + "\t" + col_string + trail + "\n"

        table_str += ");"
        table_str += "\n--========================--\n"
        if self.dialect == "MSSQL":
            table_str += F"CREATE CLUSTERED COLUMNSTORE INDEX IDX_{self.default_name} ON {self.default_name};"
            table_str += "\n--========================--\n"
            table_str += "BULK INSERT " + self.default_name + "\n"
            table_str += "FROM 'D:\\TEMP\\" + self.default_name + ".TXT'\n"
            table_str += "WITH (CODEPAGE='65001', FIRSTROW = 2,FIELDTERMINATOR = '\\t', ROWTERMINATOR = '\\n');"
        elif self.dialect == "PG":
            table_str += "COPY " + self.default_name + "\n"
            table_str += "FROM 'D:\\TEMP\\" + self.default_name + ".TXT'\n"
            # table_str += "credentials 'aws_access_key_id=xxx;aws_secret_access_key=xxx'\n"
            table_str += "DELIMITER '\\t' CSV IGNOREHEADER 1;"
        else:
            pass
        return table_str

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

        if self.show_table_command:
            self.table_command = self.get_create_table_command()
            self.log("DDL SQL Command Generated")

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
        self.print_table_command()

    def print_table_command(self):
        if self.show_table_command:
            print("--=============================--")
            print(self.table_command)
            print("--=============================--")

    def export_query_to_html(self, sql_command, html_file):
        # Time
        self.timer_start()

        # Start
        cursor = self.conn.cursor()
        cursor.execute(sql_command)
        self.log("Using SQL Command : ")
        print("--=============================--")
        print(sql_command)
        print("--=============================--")
        col_name = self.get_col_name_list(cursor)
        col_metadata = self.get_col_metadata(cursor)

        print(col_name)
        list_of_list = []
        list_of_dict = []

        rec = 0
        row = cursor.fetchone()
        while row is not None:
            rec += 1
            list_a = []
            dict_a = {}
            for i, r in enumerate(row):
                col = col_name[i]
                if r is None:
                    dict_a[col] = ""
                    list_a.append("")
                else:
                    dict_a[col] = str(r)
                    list_a.append(str(r))

            list_of_list.append(list_a)
            list_of_dict.append(dict_a)

            if rec % self.break_row_count == 0:
                self.log("{rec} records passed.".format(rec=str(rec)))
            row = cursor.fetchone()

        self.total_record = rec
        self.log(F"Total {str(rec)} records.")

        html_start = "<html>\n"
        html_end = "</html>\n"

        f = open(html_file, "w")

        f.write(html_start)

        f.write(
            """<table cellpadding="6" style="font-family:Tahoma;font-size:12px;border='1px solid black';border-collapse: collapse;">\n""")

        th_string = "<thead style='text-align:center; background-color:#DFDFDF;'><tr>"
        for c in col_name:
            th_string += F"<th style='border: 1px solid black;'>{c}</th>"
        th_string += "</tr></thead>\n"
        f.write(th_string)
        f.write("<tbody>\n")

        for row in list_of_dict:
            row_string = "<tr>"
            for r in row:
                style = ""
                if "AMT" in r:
                    style += "text-align:right;"
                row_string += F"<td style='border: 1px solid black; {style}'>{row[r]}</td>"
            row_string += "</tr>\n"
            f.write(row_string)

        f.write("</tbody>\n")
        f.write(html_end)

        f.close()

        self.log(F"Finished export to {html_file}")

        # Time
        self.timer_stop()
        cursor.close()

    def zip(self, source_file, zip_file=None):
        if not zip_file:
            # zip_file = os.path.splitext(source_file)[0] + ".zip"
            zip_file = source_file + ".zip"
        with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as z:
            z.write(source_file, os.path.basename(source_file))
            self.log("Zipped {file} to {zip}".format(file=os.path.basename(source_file), zip=zip_file))

    def gzip(self, source_file, zip_file=None):
        if not zip_file:
            zip_file = source_file + ".gz"
        with open(source_file, 'rb') as f_in, gzip.open(zip_file, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
            self.log("Gzipped {file} to {zip}".format(file=os.path.basename(source_file), zip=zip_file))

    def get_file_size(self, file):
        size = os.stat(file)[6]
        self.log("FILE : {file} / SIZE: {size} BYTES".format(file=os.path.basename(file), size=str(size)))
        return size
