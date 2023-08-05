import pandas as pd
import xlsxwriter
from datetime import datetime
import time


class ExcelFormatter():
    def __init__(self, dict_config=None, logger=None):
        self.default_font_name = "Tahoma"
        self.default_font_size = 10
        if dict_config:
            self.set_config(dict_config)

        if logger:
            self.logger = logger
        else:
            self.logger = None

    ###############
    ### LOGGING ###
    ##############

    def log(self, input_str, level=None):
        ident = "[HYPER]"
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

    ##############
    ### CONFIG ###
    ##############
    def set_config(self, dict_config):
        if dict_config.get("font-family"):
            self.default_font_name = dict_config.get("font-family")
        else:
            self.default_font_name = "Tahoma"

        if dict_config.get("font-size"):
            self.default_font_size = int(dict_config.get("font-size"))
        else:
            self.default_font_size = 10

        self.log(f"Default Font Family : {str(self.default_font_name)}")
        self.log(f"Default Font Size   : {str(self.default_font_size)}")

    ############
    ### MAIN ###
    ############

    def df_to_excel(self, df_source, file_name, sheet_name):

        df = df_source

        workbook = xlsxwriter.Workbook(file_name, {"nan_inf_to_errors": True})

        default_font_name = self.default_font_name
        default_font_size = self.default_font_size

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
        format_title.set_bg_color('#aaffcc')

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
            try:
                i = df[col].map(len).max()
            except:
                i = 20
            i = max(int(i) * 1.25, 12)
            dict_len[col] = i

        row_count = df.shape[0]
        col_count = df.shape[1]
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
                if "%" in column:
                    worksheet.set_column(i, i, default_column_width)
                else:
                    worksheet.set_column(i, i, default_column_width)

            elif column in int_list:
                worksheet.set_column(i, i, default_column_width)

            else:
                worksheet.set_column(i, i, default_column_width)
            i += 1

        worksheet.autofilter(0, 0, df.shape[0], df.shape[1] - 1)
        workbook.close()
