import os
import sys
import glob
from datetime import datetime
import pandas as pd
import numpy as np
import math
import pyodbc
import time
from tableauhyperapi import HyperProcess, Telemetry, Connection, CreateMode, NOT_NULLABLE, NULLABLE, SqlType, \
    TableDefinition, Inserter, \
    escape_name, escape_string_literal, HyperException, TableName

pd.set_option('display.float_format', lambda x: '%.4f' % x)


class HyperClass():
    def __init__(self, logger=None):
        if logger:
            self.logger = logger
        else:
            self.logger = None
        self.cs = None
        self.conn = None
        self.hyper = None
        self.hyper_conn = None
        self.try_start_count = 5
        self.sleep_time = 3
        self.cleanup = True
        self.time = None
        self.inserter_break_row_count = 10000
        self.inserter_commit_row_count = 1000000

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

    ###########################
    ### Base Function - END ###
    ###########################

    def start(self):
        if self.cleanup:
            # cp = Path(os.path.dirname(os.path.abspath(__file__))).parent
            cp = os.getcwd()
            self.log(F"Current Working Directory = {cp}")
            list_hyper_temp_file = glob.glob(str(cp) + "/hyper_db*")
            for f in list_hyper_temp_file:
                try:
                    os.remove(f)
                except Exception as e:
                    self.log(str(e), "ERROR")
            try:
                os.remove(cp + "/hyperd.log")
            except Exception as e:
                self.log(str(e), "ERROR")

            self.log("Temp files removed.")

        i = 0
        while (i <= self.try_start_count) and not self.hyper:
            try:
                self.hyper = HyperProcess(Telemetry.DO_NOT_SEND_USAGE_DATA_TO_TABLEAU)
                self.log("Hyper process started.")
            except Exception as e:
                self.log(str(e))
                self.log("Cannot start hyper, retrying.")
                time.sleep(self.sleep_time)
            i = i + 1

    def connect_file(self, hyper_file):
        self.hyper_conn = Connection(self.hyper.endpoint, hyper_file, CreateMode.NONE)
        self.log(F"Connected to {os.path.basename(hyper_file)}")

    def create_file(self, hyper_file):
        self.hyper_conn = Connection(self.hyper.endpoint, hyper_file, CreateMode.CREATE_AND_REPLACE)
        self.log(f"##############################")
        self.log(f"Create file  : {hyper_file}")
        self.log(F"Connected to : {os.path.basename(hyper_file)}")
        self.log(f"##############################")

    def detach_file(self):
        self.hyper_conn.close()
        self.log(f"****** DETACHED ******")
        self.log(F"Closing connection to file")

    def create_schema(self, schema_name):
        self.hyper_conn.catalog.create_schema(schema_name)
        self.log(F"Create Schema {schema_name}")

    def create_table(self, table_def):
        self.hyper_conn.catalog.create_table(table_def)
        self.log(F"Create Table {table_def.table_name}")

    def execute_command(self, sql_command):
        if not self.hyper_conn:
            self.log("Cannot execute command, please start Hyper Connection first.")
        else:
            try:
                self.timer_start()
                self.log("Executing Command...")
                self.log(sql_command)
                result = self.hyper_conn.execute_command(command=sql_command)
                self.log(F"Execute command success, {result} rows affected.")
                self.timer_stop()
            except Exception as e:
                self.log(str(e))
                self.log("Execute command not success.")
                self.timer_stop()

    def copy(self, table_name, file_name):
        sql_command = F'''
        COPY "Extract"."{table_name}" FROM '{file_name}'
        WITH (format csv, NULL '', delimiter '\t', header)
        '''
        self.execute_command(sql_command)

    def copy_csv(self, table_name, file_name):
        sql_command = F'''
        COPY "Extract"."{table_name}" FROM '{file_name}'
        WITH (format csv, NULL '', delimiter ',', header)
        '''
        self.execute_command(sql_command)

    def query(self, sql_command):
        if not self.hyper_conn:
            self.log("Cannot execute command, please start Hyper Connection first.")
        else:
            try:
                self.log("Executing Command...")
                self.log(sql_command)
                result = self.hyper_conn.execute_list_query(query=sql_command)
                return result
            except Exception as e:
                self.log(str(e))
                self.log("Execute command not success.")

    def create_table_from_cols(self, table_name, cols):
        if table_name:
            table_name = table_name
        else:
            table_name = "Extract"
        self.log(F"Input Columns : {str(cols)}")

        list_col = []
        col_def = None

        for i, c in enumerate(cols):
            col_name = c[0]
            col_string = c[1].upper()

            if col_string == "STR":
                c_len = c[2]
                if c_len == 0:
                    c_len = 2
                elif c_len >= 4000:
                    c_len = 4000
                else:
                    c_len = c_len * 2

                col_def = TableDefinition.Column(col_name, SqlType.varchar(c_len))

            elif col_string == "DATETIME.DATETIME":
                col_def = TableDefinition.Column(col_name, SqlType.timestamp())
            elif col_string == "DATETIME.DATE":
                col_def = TableDefinition.Column(col_name, SqlType.date())
            elif col_string == "DECIMAL.DECIMAL":
                col_def = TableDefinition.Column(col_name, SqlType.double())
            elif col_string == "FLOAT":
                col_def = TableDefinition.Column(col_name, SqlType.double())
            elif col_string == "BYTEARRAY":
                col_def = TableDefinition.Column(col_name, SqlType.varchar(1000))
            elif col_string == "INT":
                c_len = c[2]
                if c_len > 10:
                    col_def = TableDefinition.Column(col_name, SqlType.big_int())
                else:
                    col_def = TableDefinition.Column(col_name, SqlType.int())
            list_col.append(col_def)

        table_def = TableDefinition(TableName('Extract', table_name), list_col)
        self.log("Finished Convert Cursor Columns to Hyper Table Definition")
        self.create_table(table_def)

    def create_table_def_from_cols(self, table_name, cols):
        if table_name:
            table_name = table_name
        else:
            table_name = "Extract"
        self.log(F"Input Columns : {str(cols)}")

        list_col = []
        col_def = None

        for i, c in enumerate(cols):
            col_name = c[0]
            col_string = c[1].upper()

            if col_string == "STR":
                c_len = c[2]
                if c_len == 0:
                    c_len = 2
                elif c_len >= 4000:
                    c_len = 4000
                else:
                    c_len = c_len * 2

                col_def = TableDefinition.Column(col_name, SqlType.varchar(c_len))

            elif col_string == "DATETIME.DATETIME":
                col_def = TableDefinition.Column(col_name, SqlType.timestamp())
            elif col_string == "DATETIME.DATE":
                col_def = TableDefinition.Column(col_name, SqlType.date())
            elif col_string == "DECIMAL.DECIMAL":
                col_def = TableDefinition.Column(col_name, SqlType.double())
            elif col_string == "FLOAT":
                col_def = TableDefinition.Column(col_name, SqlType.double())
            elif col_string == "BYTEARRAY":
                col_def = TableDefinition.Column(col_name, SqlType.varchar(1000))
            elif col_string == "INT":
                c_len = c[2]
                if c_len > 10:
                    col_def = TableDefinition.Column(col_name, SqlType.big_int())
                else:
                    col_def = TableDefinition.Column(col_name, SqlType.int())
            list_col.append(col_def)

        table_def = TableDefinition(TableName('Extract', table_name), list_col)
        self.log("Finished Convert Cursor Columns to Hyper Table Definition")
        return table_def

    def get_create_hyper_table_command_from_cols(self, cols, table_name=None):
        if table_name:
            table_name = table_name
        else:
            table_name = "Extract"

        hyper_start_str = F"table = TableDefinition(TableName('Extract', '{table_name}'), [\n"
        hyper_end_str = F"])"
        hyper_str = hyper_start_str

        trail = ","
        for i, c in enumerate(cols):
            if i == len(cols) - 1:
                trail = ""

            col_string = c[1].upper()
            if col_string == "STR":
                c_len = c[2]
                if c_len == 0:
                    c_len = 2
                elif c_len >= 4000:
                    c_len = 4000
                else:
                    c_len = c_len * 2
                col_string = "varchar({len})".format(len=str(c_len))
            elif col_string == "DATETIME.DATETIME":
                col_string = "timestamp()"
            elif col_string == "DATETIME.DATE":
                col_string = "date()"
            elif col_string == "DECIMAL.DECIMAL":
                col_string = "double()"
            elif col_string == "FLOAT":
                col_string = "double()"
            elif col_string == "BYTEARRAY":
                col_string = "varchar(1000)"
            elif col_string == "INT":
                c_len = c[2]
                if c_len > 10:
                    col_string = "big_int()"
                else:
                    col_string = "int()"

            hyper_str += F"\tTableDefinition.Column('{c[0]}', SqlType.{col_string}){trail}\n"

        hyper_str += hyper_end_str
        hyper_str += F"""\n--==============
        COPY "Extract"."{table_name}" FROM '{table_name}.txt'
        WITH (format csv, NULL '', delimiter '\\1', escape '\\\\', quote '\\2')"""
        print(hyper_str)
        return hyper_str

    ###############################
    ### ODBC FUNCTION START
    ###############################

    def odbc_connect(self, cs):
        if cs:
            self.cs = cs
        try:
            self.conn = pyodbc.connect(self.cs)
            self.log("Connect to database successfully.")
        except Exception as e:
            self.log("Cannot connect to database")
            self.log(F"{str(e)}")

    def odbc_execute(self, sql_command):
        sql_txt = sql_command.replace("\n", " ").replace("\r", " ").strip()
        self.log(F"Using {sql_txt}")
        self.timer_start()
        try:
            cursor = self.conn.cursor()
            cursor.commit()
            cursor.execute(sql_command)
            cursor.commit()
            cursor.close()
        except Exception as e:
            self.log(F"{str(e)}", "ERROR")
            cursor.rollback()
            cursor.close()
        self.timer_stop()

    def get_col_metadata(self, cursor):
        cols = [[column[0], str(column[1]).replace("<class '", "").replace("'>", ""), column[4], column[5]] for column
                in
                cursor.description]
        return cols

    def get_cursor_definition(self, sql_command):
        self.log("Starting Query")
        self.timer_start()
        cursor = self.conn.cursor()
        cursor.commit()
        cursor.execute(sql_command)
        self.log("Get definition using this SQL Command : ")
        self.log(sql_command)
        col_metadata = self.get_col_metadata(cursor)
        self.log(str(col_metadata))
        cursor.close()
        self.timer_stop()
        return col_metadata

    def create_table_from_sql_command(self, table_name, sql_command):
        cols = self.get_cursor_definition(sql_command)
        self.log(f"##############################")
        self.log(f"CREATE TABLE : {table_name}")
        self.log(f"##############################")
        self.create_table_from_cols(table_name, cols)

    def create_table_def_from_sql_command(self, table_name, sql_command):
        cols = self.get_cursor_definition(sql_command)
        table_def = self.create_table_def_from_cols(table_name, cols)
        return table_def

    def get_hyper_table_command_from_sql_command(self, table_name, sql_command):
        cols = self.get_cursor_definition(sql_command)
        self.get_create_hyper_table_command_from_cols(cols, table_name)

    def streaming_insert_v1(self, table_name, sql_command, create_table=None):
        if create_table:
            self.create_table_from_sql_command(table_name, sql_command)
        else:
            pass

        cursor = self.conn.cursor()
        cursor.commit()
        cursor.execute(sql_command)
        rec = 0

        inserter = Inserter(self.hyper_conn, TableName('Extract', table_name))

        row = cursor.fetchone()
        while row is not None:
            rec += 1
            if rec % self.inserter_break_row_count == 0:
                self.log(F"{str(rec)} records passed")
            inserter.add_row([c for c in row])
            if rec % self.inserter_commit_row_count == 0:
                self.log(F"Committing at {str(rec)} records")
                inserter.execute()
                inserter = Inserter(self.hyper_conn, TableName('Extract', table_name))

            row = cursor.fetchone()

        self.log(F"Final Commit")
        self.log(F"Total {str(rec)} records")
        inserter.execute()
        cursor.close()

        self.log("Finished Streaming data to Hyper File")

    def streaming_insert_v2(self, table_name, sql_command, create_table=None):
        if create_table:
            self.create_table_from_sql_command(table_name, sql_command)
        else:
            pass

        cursor = self.conn.cursor()
        cursor.commit()
        cursor.execute(sql_command)
        rec = 0

        inserter = Inserter(self.hyper_conn, TableName('Extract', table_name))

        list_of_row = []
        row = cursor.fetchone()
        while row is not None:
            rec += 1
            list_of_row.append([c for c in row])
            if rec % self.inserter_break_row_count == 0:
                self.log(F"Read {str(rec)} records")
                inserter.add_rows(rows=list_of_row)
                list_of_row = []
            if rec % self.inserter_commit_row_count == 0:
                self.log(F"Committing at {str(rec)} records")
                inserter.execute()
                inserter = Inserter(self.hyper_conn, TableName('Extract', table_name))

            row = cursor.fetchone()

        inserter.add_rows(rows=list_of_row)
        del list_of_row
        self.log(F"Final Commit")
        self.log(F"Total {str(rec)} records")
        inserter.execute()
        cursor.close()

        self.log("Finished Streaming data to Hyper File")

    def streaming_insert(self, table_name, sql_command, create_table=None, batch_size=None):
        if create_table:
            self.create_table_from_sql_command(table_name, sql_command)
        else:
            pass

        cursor = self.conn.cursor()
        cursor.commit()
        cursor.execute(sql_command)
        rec = 0

        inserter = Inserter(self.hyper_conn, TableName('Extract', table_name))
        if batch_size:
            break_row_count = batch_size
        else:
            break_row_count = 10000

        self.log(f"Batch Size : {str(break_row_count)}")

        while True:
            rows = cursor.fetchmany(break_row_count)
            if not rows:
                break
            else:
                l = len(rows)
                rec += l
                self.log(F"Read {str(rec)} records")
                inserter.add_rows(rows=rows)

        self.log(F"Final Commit")
        self.log(F"Total {str(rec)} records")
        inserter.execute()
        cursor.close()

        self.log("Finished Streaming data to Hyper File")

    def query_to_hyper(self, hyper_file, table_name, sql_command, batch_size=None):
        self.start()
        self.create_file(hyper_file)
        self.create_schema('Extract')
        # sql_command_zero = f"SELECT * FROM ( {sql_command} ) TMP WHERE 0=1"
        # self.create_table_from_sql_command(table_name, sql_command_zero)
        self.streaming_insert('Extract', sql_command, create_table=True, batch_size=batch_size)
        self.detach_file()
        self.stop()

    ###############################
    ### ODBC FUNCTION STOP
    ###############################

    ###############################
    ### PANDAS FUNCTION START
    ###############################

    def create_table_from_df(self, table_name, df):
        list_columns = list(df.columns)
        list_dtype = [str(a) for a in df.dtypes]
        list_coltype = list(zip(list_columns, list_dtype))
        self.log(F"DataFrame dtypes : {str(list_coltype)}")
        list_col = []
        for c in list_coltype:
            cname = c[0]
            ctype = c[1]
            if ctype == "int64":
                list_col.append(TableDefinition.Column(cname, SqlType.big_int()))
            elif ctype == "int32":
                list_col.append(TableDefinition.Column(cname, SqlType.int()))
            elif ctype == "object":
                list_col.append(TableDefinition.Column(cname, SqlType.varchar(8000)))
            elif ctype == "float64":
                list_col.append(TableDefinition.Column(cname, SqlType.double()))
            elif ctype == "bool":
                list_col.append(TableDefinition.Column(cname, SqlType.bool()))
            else:
                list_col.append(TableDefinition.Column(cname, SqlType.varchar(1000)))

        table_def = TableDefinition(TableName('Extract', table_name), list_col)
        self.log("Finished Convert DF Columns to Hyper Table Definition")
        self.create_table(table_def)

    def get_create_hyper_table_command_from_df(self, df, table_name=None):
        if table_name:
            table_name = table_name
        else:
            table_name = "Extract"

        list_columns = list(df.columns)
        list_dtype = [str(a) for a in df.dtypes]
        list_coltype = list(zip(list_columns, list_dtype))
        self.log(F"DataFrame dtypes : {str(list_coltype)}")

        hyper_start_str = F"table = TableDefinition(TableName('Extract', '{table_name}'), [\n"
        hyper_end_str = F"])"
        hyper_str = hyper_start_str

        trail = ","
        for i, c in enumerate(list_coltype):
            col_string = ""
            if i == len(list_coltype) - 1:
                trail = ""
            cname = c[0]
            ctype = c[1]
            if ctype == "int64":
                col_string = "big_int()"
            elif ctype == "int32":
                col_string = "int()"
            elif ctype == "float64":
                col_string = "double()"
            elif ctype == "bool":
                col_string = "bool()"
            elif ctype == "datetime64[ns]":
                col_string = "timestamp()"
            else:
                col_string = "varchar(2000)"

            hyper_str += F"\tTableDefinition.Column('{cname}', SqlType.{col_string}){trail}\n"

        hyper_str += hyper_end_str
        hyper_str += F"""\n--==============
        COPY "Extract"."{table_name}" FROM '{table_name}.txt'
        WITH (format csv, NULL '', delimiter ',', escape '\\\\')"""
        print(hyper_str)
        return hyper_str

    def df_insert_to_hyper(self, table_name, df, create_table=None):
        if create_table:
            self.create_table_from_df(table_name, df)
        else:
            pass
        list_dtype = [str(a) for a in df.dtypes]
        list_of_rows = df.values.tolist()
        with Inserter(self.hyper_conn, TableName('Extract', table_name)) as inserter:
            row_count = 0
            for row in list_of_rows:
                row_count += 1
                for i, d in enumerate(list_dtype):
                    if d == "int64" or d == "int32":
                        if row[i] == "nan":
                            row[i] = None
                        else:
                            row[i] = int(row[i])
                    if d == "float64":
                        if np.isnan(row[i]):
                            row[i] = None
                    elif d == "object":
                        row[i] = str(row[i])
                        if row[i] == "nan":
                            row[i] = None
                    elif row[i] == np.nan:
                        row[i] = None
                    else:
                        pass
                # print(df.columns)
                # print(row)
                inserter.add_row(row)
            inserter.execute()
            self.log(F"Total {str(row_count)} rows inserted.")
        self.log("Finished Convert DataFrame to Hyper File")

    ###############################
    ### PANDAS FUNCTION STOP
    ###############################

    def stop(self):
        if self.hyper_conn:
            try:
                self.hyper_conn.close()
                self.log("Closing Hyper Connection.")
            except Exception as e:
                self.log(str(e))
        if self.hyper:
            try:
                self.hyper.close()
                self.log("Closing Hyper Process.")
            except Exception as e:
                self.log(str(e))
