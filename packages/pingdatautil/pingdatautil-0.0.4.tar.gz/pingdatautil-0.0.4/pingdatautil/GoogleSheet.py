from datetime import datetime
import time
import csv
import os
import gspread
import codecs
from oauth2client.service_account import ServiceAccountCredentials

os.environ["PYTHONIOENCODING"] = "utf-8"


class GoogleSheet:
    def __init__(self, logger=None):
        if logger:
            self.logger = logger
        else:
            self.logger = None
        self.time = None
        self.client = None
        self.workbook = None

    ###############
    ### LOGGING ###
    ##############

    def log(self, input_str, level=None):
        ident = "[GOOGLESHEET]"
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

    #####################
    #### MAIN CLASS #####
    #####################

    def authenticate_with_client_secret_file(self, client_secret_file):
        self.authenticate_sheet_with_client_secret_file(client_secret_file)

    def authenticate_sheet_with_client_secret_file(self, client_secret_file):
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(client_secret_file, scope)
        self.client = gspread.authorize(creds)

    def open_sheet(self, sheet_name):
        self.workbook = self.client.open(sheet_name)

    def connect_sheet(self, sheet_name):
        self.open_sheet(sheet_name)

    def authenticate_open_sheet(self, client_secret_file, sheet_name):
        self.authenticate_sheet_with_client_secret_file(client_secret_file)
        self.open_sheet(sheet_name)

    def authenticate_connect_sheet(self, client_secret_file, sheet_name):
        self.authenticate_sheet_with_client_secret_file(client_secret_file)
        self.connect_sheet(sheet_name)

    def list_sheets(self, page_size=None):
        if not page_size:
            page_size = 100
        list_items_all = []
        page_token = None
        while True:
            try:
                param = {}
                if page_token:
                    param['pageToken'] = page_token
                    self.log(F"Continue fetching...")
                self.log(F"Fetching {str(page_size)} items")
                files = self.service.files().list(pageSize=page_size,
                                                  fields="nextPageToken, files(id, name, mimeType, size, parents, modifiedTime)",
                                                  q='mimeType="application/vnd.google-apps.spreadsheet"').execute()
                for item in files['files']:
                    list_items_all.append(item)
                page_token = files.get('nextPageToken')
                if not page_token:
                    self.log("Finished fetching...")
                    break
            except Exception as e:
                print(str(e))
        self.log(F"Total {str(len(list_items_all))} found.")
        return list_items_all

    def discover_sheet(self, sheet_id):
        self.log(F"Discover sheet_id : {sheet_id}")
        # result = self.sheets.spreadsheets().values().get(spreadsheetId=sheet_id, range=sheet_name).execute()
        sheet_metadata = self.sheets.spreadsheets().get(spreadsheetId=sheet_id).execute()
        sheets = sheet_metadata.get('sheets', '')
        for s in sheets:
            sheet_m = s.get("properties", {})
            self.log(str(sheet_m))

    def download_sheet(self, sheet_id, sheet_name=None, file_name=None):
        self.log(F"Downloading sheet_id : {sheet_id} / {sheet_name}")
        result = self.sheets.spreadsheets().values().get(spreadsheetId=sheet_id, range=sheet_name).execute()

        output_file = file_name
        with open(output_file, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f, delimiter='\t', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
            res = result.get('values')
            if res:
                writer.writerows(res)
            self.log(F"Saved to {output_file}")
        f.close()
        self.log(F"Done.")

    def upload_csv(self, csv_file, sheet_name):
        self.log("===============================")
        self.log(f"Importing : {csv_file}")
        size_kb = os.path.getsize(csv_file) / 1000
        size_str = "{:,.2f}".format(size_kb)
        self.log(f"File Size : {size_str} KB")
        self.log(f"Target Sheet : {sheet_name}")

        sheetId = self.workbook.worksheet(sheet_name)._properties['sheetId']
        body = {
            "requests": [
                {
                    "deleteRange": {
                        "range": {
                            "sheetId": sheetId
                        },
                        "shiftDimension": "ROWS"
                    }
                }
            ]
        }
        self.workbook.batch_update(body)

        f = codecs.open(csv_file, 'r', encoding='utf-8')
        self.workbook.values_update(
            sheet_name,
            params={'valueInputOption': 'USER_ENTERED'},
            body={'values': list(csv.reader(f))}
        )
        f.close()
        self.log("Done")
