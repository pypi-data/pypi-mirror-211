import jaydebeapi
import pyodbc
import pandas as pd
import numpy as np
import os, sys
import glob
import warnings
import codecs
import xlsxwriter
import time
from datetime import datetime

warnings.filterwarnings("ignore", category=UserWarning)


class UnitTest():
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

        self.ident = "[UNIT-TEST]"
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
    def query(self, query_str):
        df = pd.read_sql_query(query_str, self.conn)
        print(df)

    def get_current_path(self):
        current_path = os.path.dirname(os.path.abspath(__file__))
        return current_path

    def get_parent_path(self):
        parent_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        return parent_path

    def get_path(self, input_path):
        parent_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        join_path = os.path.join(parent_path, input_path)
        return join_path

    def list_file_from_path(self, input_path, wildcard=None):
        if wildcard:
            list_path = input_path + "/" + wildcard
        else:
            list_path = input_path + "/*.*"
        list_file = glob.glob(list_path)
        self.log(f"File List : {str(list_file)}")
        return list_file

    def read_file(self, input_file):
        with codecs.open(input_file, 'r', encoding="utf-8") as f:
            str = f.read().rstrip()
        return str

    def query_sql_from_path(self, input_path, wildcard=None):
        list_file_from_path = self.list_file_from_path(input_path, wildcard)
        for sql_file in list_file_from_path:
            query_str = self.read_file(sql_file)
            self.query(query_str)

    def query_to_excel(self, excel_file, query_str):
        df = pd.read_sql_query(query_str, self.conn)
        print(df)
        df.to_excel(excel_file, index=False)

    def query_to_excel_from_path(self, excel_path, sql_path):
        query_str = self.read_file(sql_path)
        df = pd.read_sql_query(query_str, self.conn)
        print(df)

    def query_to_excel_with_sql(self, excel_file, sql_file):
        workbook = pd.ExcelWriter(excel_file, engine='xlsxwriter')
        query_str = self.read_file(sql_file)
        df = pd.read_sql_query(query_str, self.conn)
        df.to_excel(workbook, sheet_name="DATA", index=False)
        df1 = pd.read_csv(sql_file, header=None, sep="\x01")
        df1.to_excel(workbook, sheet_name="SQL", index=False, header=False)
        workbook.close()

    def query_to_excel_multi_sheet_with_sql(self, excel_file, list_sql_file,
                                            default_font_name=None,
                                            default_font_size=None,
                                            header_color=None):

        # New Workbook

        workbook = xlsxwriter.Workbook(excel_file, {"nan_inf_to_errors": True})

        if not default_font_name:
            default_font_name = "Tahoma"
        if not default_font_size:
            default_font_size = 10
        if not header_color:
            header_color = "#aaffcc"
        workbook.formats[0].set_font_size(default_font_size)
        workbook.formats[0].set_font(default_font_name)

        format_date = workbook.add_format({
            'num_format': 'yyyy-mm-dd',
            'font_name': default_font_name,
            'font_size': default_font_size
        })
        format_int = workbook.add_format({
            'num_format': '#,##0',
            'font_name': default_font_name,
            'font_size': default_font_size
        })
        format_num = workbook.add_format({
            'num_format': '#,##0.00',
            'font_name': default_font_name,
            'font_size': default_font_size
        })
        format_pct = workbook.add_format({
            'num_format': '#,##0.00%',
            'font_name': default_font_name,
            'font_size': default_font_size
        })
        format_num_red = workbook.add_format({
            'num_format': '#,##0.00',
            'font_color': '#ff0000',
            'font_name': default_font_name,
            'font_size': default_font_size
        })
        format_pct_red = workbook.add_format({
            'num_format': '#,##0.00%',
            'font_color': '#ff0000',
            'font_name': default_font_name,
            'font_size': default_font_size
        })
        format_text_left = workbook.add_format({
            'num_format': '@',
            'text_h_align': 1,
            'font_name': default_font_name,
            'font_size': default_font_size
        })
        format_text_right = workbook.add_format({
            'num_format': '@',
            'text_h_align': 3,
            'font_name': default_font_name,
            'font_size': default_font_size
        })
        format_title = workbook.add_format({
            'text_v_align': 2,
            'text_h_align': 2,
            'text_wrap': True,
            'bold': True,
            'font_name': default_font_name,
            'font_size': default_font_size
        })
        format_title.set_border(1)
        format_title.set_font_color('black')
        format_title.set_bg_color(header_color)

        # START LOOP

        for sql_file in list_sql_file:
            sheet_name = os.path.basename(sql_file).split(".")[0]
            query_str = self.read_file(sql_file)
            df = pd.read_sql_query(query_str, self.conn)

            worksheet = workbook.add_worksheet(sheet_name)

            list_dtype = [str(t) for t in df.dtypes]
            list_dtype_group = []

            for d in list_dtype:
                if "datetime" in d:
                    list_dtype_group.append("datetime")
                elif "int" in d:
                    list_dtype_group.append("int")
                elif "float" in d:
                    list_dtype_group.append("float")
                elif "object" in d:
                    list_dtype_group.append("object")
                else:
                    list_dtype_group.append("other")

            dict_dt = dict(zip(df.columns, list_dtype))
            dict_dt_group = dict(zip(df.columns, list_dtype_group))

            dict_format = {}
            for key, value in dict_dt_group.items():
                if dict_dt_group.get(key) == "int":
                    dict_format[str(key)] = format_int
                elif dict_dt_group.get(key) == "float":
                    dict_format[str(key)] = format_num
                elif dict_dt_group.get(key) == "object":
                    if "pct" in str(key).lower():
                        dict_format[str(key)] = format_text_right
                    else:
                        dict_format[str(key)] = format_text_left
                elif dict_dt_group.get(key) == "datetime":
                    dict_format[str(key)] = format_date
                else:
                    dict_format[str(key)] = format_text_left

            string_list = df.select_dtypes(include=["object"]).columns
            float_list = df.select_dtypes(include=["float64", "float"]).columns
            int_list = df.select_dtypes(include=["int64", "int"]).columns

            dict_len = {}

            for col in string_list:
                clen = len(col)
                try:
                    i = df[col].map(len).max()
                except:
                    i = 20
                i = max(i, clen)
                i = max(int(i) * 1.25, 12)
                dict_len[col] = i

            for col in int_list:
                clen = len(col)
                try:
                    i = np.ceil(np.log(df[col].max()))
                except:
                    i = 20
                i = max(i, clen)
                i = max(int(i) * 1.25, 12) + 3
                dict_len[col] = i

            for col in float_list:
                clen = len(col)
                try:
                    i = np.ceil(np.log(df[col].max()))
                except:
                    i = 20
                i = max(i, clen)
                i = max(int(i) * 1, 12) + 3
                dict_len[col] = i

            self.log(str(dict_len))

            row_count = df.shape[0]
            self.log(sheet_name + " - Row Count: " + str(row_count))
            row = 0
            col = 0

            for i, colname in enumerate(df.columns):
                worksheet.write(row, col + i, colname, format_title)

            start_row = 1
            for rx in range(0, row_count):
                for cx, colname in enumerate(df.columns):
                    if (df.iloc[rx, cx] is not None) and (not pd.isnull(df.iloc[rx, cx])):
                        worksheet.write(start_row + rx, cx, df.iloc[rx, cx], dict_format.get(colname))

            i, default_column_width = 0, 12

            for column in df.columns:
                if column in string_list:
                    if column in dict_len:
                        len1 = dict_len[column]
                    else:
                        len1 = default_column_width
                    worksheet.set_column(i, i, len1)

                elif column in float_list:
                    if column in dict_len:
                        len1 = dict_len[column]
                    elif "%" in column:
                        worksheet.set_column(i, i, default_column_width)
                    else:
                        len1 = default_column_width
                    worksheet.set_column(i, i, len1)

                elif column in int_list:
                    if column in dict_len:
                        len1 = dict_len[column]
                    else:
                        len1 = default_column_width
                    worksheet.set_column(i, i, len1)

                else:
                    worksheet.set_column(i, i, default_column_width)
                i += 1

            worksheet.autofilter(0, 0, df.shape[0], df.shape[1] - 1)

            worksheet = workbook.add_worksheet(sheet_name + "_SQL")
            df = pd.read_csv(sql_file, header=None, sep="\x01")
            start_row = 0
            row_count = df.shape[0]

            for rx in range(0, row_count):
                if (df.iloc[rx, 0] is not None) and (not pd.isnull(df.iloc[rx, 0])):
                    worksheet.write(start_row + rx, 0, df.iloc[rx, 0], format_text_left)

        workbook.close()
