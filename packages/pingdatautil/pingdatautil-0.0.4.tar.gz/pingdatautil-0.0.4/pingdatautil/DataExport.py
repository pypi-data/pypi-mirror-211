import pyodbc
import jaydebeapi
import os
import sys
import time
from datetime import datetime
import re
import shutil
import gzip
import zipfile
import csv
import codecs


class DataExport():

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

        self.ident = "[DATA-EXPORT]"
        self.separator = "\t"
        self.time = None
        self.time_start = None
        self.time_end = None

        ## Data Export

        self.dialect = "MSSQL"
        self.total_record = 0
        self.total_time = 0
        self.break_row_count = 5000
        self.multiply_varchar = 1
        self.varchar_max = 4000
        self.show_header = True
        self.cols = None
        self.verbose = False
        self.need_clean = True
        self.show_table_command = None
        self.with_data_date_column = None
        self.with_row_id_column = None
        self.default_name = "EXPORT"

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
        self.log("===== SQL Command =====")
        self.log(input_sql)
        self.log("========================")

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

    ####################
    ### ZIP FUNCTION ###
    ####################
    def zip(self, source_file, zip_file=None):
        if not zip_file:
            # zip_file = os.path.splitext(source_file)[0] + ".zip"
            zip_file = source_file + ".zip"
        with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as z:
            z.write(source_file, os.path.basename(source_file))
            self.log("Zipped {file} to {zip}".format(file=os.path.basename(source_file), zip=zip_file))
        self.get_file_size(zip_file)

    def gzip(self, source_file, zip_file=None):
        if not zip_file:
            zip_file = source_file + ".gz"
        with open(source_file, 'rb') as f_in, gzip.open(zip_file, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
            self.log("Gzipped {file} to {zip}".format(file=os.path.basename(source_file), zip=zip_file))
        self.get_file_size(zip_file)

    def get_file_size(self, file):
        size = os.stat(file)[6]
        self.log("{file} / Size: {size} bytes".format(file=os.path.basename(file), size=str(size)))
        return size

    ##########################
    ### CONN UTIL FUNCTION ###
    ##########################

    def get_col_name_list(self, cursor):
        col_name = [column[0] for column in cursor.description]
        if self.with_row_id_column:
            col_name.append(self.with_row_id_column)
        if self.with_data_date_column:
            col_name.append(self.with_data_date_column)
        return col_name

    def get_col_metadata(self, cursor):
        cols = [[column[0], str(column[1]).replace("<class '", "").replace("'>", ""), column[4], column[5]] for column
                in cursor.description]
        if self.with_row_id_column:
            cols.append([self.with_row_id_column, 'bigint', None, None])
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
    ### UTILITY FUNCTION ####
    #########################

    def get_create_table_command(self, file_name=None, file_separator=None):
        table_str = "DROP TABLE " + self.default_name + ";\n"
        table_str += "CREATE TABLE " + self.default_name + " (\n"
        cols = self.cols
        self.log(F"Column Description : {str(cols)}")

        trail = ","
        for i, c in enumerate(cols):
            if i == len(cols) - 1:
                trail = ""

            col_string = c[1].upper()
            if self.dialect == "MSSQL":
                if col_string == "STR" or "VARCHAR" in col_string:
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
                if col_string == "STR" or "VARCHAR" in col_string:
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

        if not file_name:
            file_name = "D:\\TEMP\\EXPORT.TXT"
        if not file_separator:
            file_separator = self.separator

        if file_separator == "\t":
            sep_str = "\\t"
        elif file_separator == "\x01":
            sep_str = "\\x01"
        elif file_separator == "\x02":
            sep_str = "\\x02"
        else:
            sep_str = file_separator

        table_str += ");"
        table_str += "\n--========================--\n"
        if self.dialect == "MSSQL":
            table_str += F"CREATE CLUSTERED COLUMNSTORE INDEX IDX_{self.default_name} ON {self.default_name};"
            table_str += F"\n--========================--\n"
            table_str += F"BULK INSERT " + self.default_name + "\n"
            table_str += F"FROM '{file_name}'\n"
            table_str += F"WITH (CODEPAGE='65001', FIRSTROW = 2, FIELDTERMINATOR = '{sep_str}', ROWTERMINATOR = '\\n');"
        elif self.dialect == "PG":
            table_str += F"COPY " + self.default_name + "\n"
            table_str += F"FROM '{file_name}'\n"
            # table_str += "credentials 'aws_access_key_id=xxx;aws_secret_access_key=xxx'\n"
            table_str += F"DELIMITER '{sep_str}' CSV IGNOREHEADER 1;"
        else:
            pass
        return table_str

    #########################
    ### EXPORT FUNCTION #####
    #########################

    def export_query_to_text(self, sql_command, output_file, separator=None, compress=None):
        self.log("Start Export")
        self.log_sql(sql_command)

        self.timer_start()
        # data_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        data_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Start
        cursor = self.conn.cursor()
        cursor.execute(sql_command)
        # print(cursor.description)
        col_name = self.get_col_name_list(cursor)
        col_metadata = self.get_col_metadata(cursor)
        self.cols = col_metadata

        list_string_column = []
        for i, col in enumerate(col_metadata):
            if col[1] == "str":
                list_string_column.append(i)

        if not separator:
            separator = self.separator

        if separator == "\t":
            sep_str = "\\t"
        elif separator == "\x01":
            sep_str = "\\x01"
        elif separator == "\x02":
            sep_str = "\\x02"
        else:
            sep_str = separator

        self.log(f"Separator is : {sep_str}")

        f = codecs.open(output_file, mode="w+", encoding="utf-8")
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
                            row[j] = row[j].strip().replace("\t", "").replace("\n", "").replace("\r", "").replace(
                                separator, "")

            if rec % self.break_row_count == 0:
                self.log("{rec} records passed.".format(rec=str(rec)))
            if self.verbose:
                # self.testrow = row
                # print(row)
                print(*row, sep=separator)

            if self.with_data_date_column and not self.with_row_id_column:
                csv.writer(f, quoting=csv.QUOTE_NONE, escapechar='\\', delimiter=separator).writerow(
                    list(row) + [data_date])
            elif not self.with_data_date_column and self.with_row_id_column:
                csv.writer(f, quoting=csv.QUOTE_NONE, escapechar='\\', delimiter=separator).writerow(
                    list(row) + [rec])
            elif self.with_data_date_column and self.with_row_id_column:
                csv.writer(f, quoting=csv.QUOTE_NONE, escapechar='\\', delimiter=separator).writerow(
                    list(row) + [rec, data_date])
            else:
                csv.writer(f, quoting=csv.QUOTE_NONE, escapechar='\\', delimiter=separator).writerow(row)

            row = cursor.fetchone()

        self.total_record = rec
        self.log("Total {rec} records.".format(rec=str(rec)))
        self.log("Finished export to {file}".format(file=output_file))

        # Time
        self.timer_stop()
        f.close()
        cursor.close()

        if self.show_table_command:
            self.table_command = self.get_create_table_command(file_name=output_file, file_separator=separator)
            self.log("DDL SQL Command Generated")
            self.print_table_command()

        if compress:

            if compress.lower() == "zip":
                output_file_c = output_file + ".zip"
                self.zip(output_file, output_file_c)
            elif compress.lower() in ["gzip", "gz"]:
                output_file_c = output_file + ".gz"
                self.gzip(output_file, output_file_c)
            else:
                self.log("Will not compress anything.")

    def print_table_command(self):
        if self.show_table_command:
            print("--=============================--")
            print(self.table_command)
            print("--=============================--")

    #########################
    ### HTML FUNCTION ###
    #########################

    def export_query_to_html(self, sql_command, html_file):
        # Time
        self.timer_start()
        data_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Start
        cursor = self.conn.cursor()
        cursor.execute(sql_command)
        self.log_sql(sql_command)
        col_name = self.get_col_name_list(cursor)
        col_metadata = self.get_col_metadata(cursor)

        self.log(f"List of column name {str(col_name)}")
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

            if self.with_data_date_column and not self.with_row_id_column:
                dict_a[self.with_data_date_column] = data_date
                list_a.append(data_date)
            elif not self.with_data_date_column and self.with_row_id_column:
                dict_a[self.with_row_id_column] = rec
                list_a.append(rec)
            elif self.with_data_date_column and self.with_row_id_column:
                dict_a[self.with_row_id_column] = rec
                list_a.append(rec)
                dict_a[self.with_data_date_column] = data_date
                list_a.append(data_date)
            else:
                pass

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
                r = r.lower().strip()
                style = ""
                if "amt" in r or "amount" in r or "_id" in r:
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
