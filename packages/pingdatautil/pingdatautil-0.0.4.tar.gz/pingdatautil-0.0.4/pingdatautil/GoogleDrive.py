from datetime import datetime
import time
import csv
import codecs
import io
import shutil
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.discovery import build


class GoogleDrive:
    def __init__(self, logger=None):
        if logger:
            self.logger = logger
        else:
            self.logger = None
        self.time = None
        self.service = None
        self.sheets = None


    ###############
    ### LOGGING ###
    ##############

    def log(self, input_str, level=None):
        ident = "[GOOGLEDRIVE]"
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
        self.authenticate_drive_with_client_secret_file(client_secret_file)

    def authenticate_drive_with_client_secret_file(self, client_secret_file):
        SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]
        credentials = ServiceAccountCredentials.from_json_keyfile_name(client_secret_file, SCOPES)
        try:
            self.service = build('drive', 'v3', credentials=credentials)
            self.log("Authenticated : Drive API")
        except Exception as e:
            self.log(F"{str(e)}")
    def authenticate_sheet_with_client_secret_file(self, client_secret_file):
        SCOPES = ["https://www.googleapis.com/auth/drive.readonly",
                  "https://www.googleapis.com/auth/spreadsheets.readonly"]
        credentials = ServiceAccountCredentials.from_json_keyfile_name(client_secret_file, SCOPES)
        try:
            self.sheets = build('sheets', 'v4', credentials=credentials)
            self.log("Authenticated : Sheets API")
        except Exception as e:
            self.log(F"{str(e)}")

    def list_files(self, page_size=None):
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
                                                  fields="nextPageToken, files(id, name, mimeType, size, parents, modifiedTime)").execute()
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

    def download_file(self, file_id, local_file_name):
        self.log(F"Downloading file_id : {file_id}")
        self.log(F"Save Path : {local_file_name}")
        request = self.service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
        fh.seek(0)
        with open(local_file_name, 'wb') as f:
            shutil.copyfileobj(fh, f, length=131072)

    def discover_sheet(self, sheet_id):
        self.log(F"Discover sheet_id : {sheet_id}")
        # result = self.sheets.spreadsheets().values().get(spreadsheetId=sheet_id, range=sheet_name).execute()
        sheet_metadata = self.sheets.spreadsheets().get(spreadsheetId=sheet_id).execute()
        sheets = sheet_metadata.get('sheets', '')
        for s in sheets:
            sheet_m = s.get("properties", {})
            self.log(str(sheet_m))

    def download_sheet(self, sheet_id, sheet_name=None, local_file_name=None):
        self.log(F"Downloading sheet_id : {sheet_id} / {sheet_name}")
        result = self.sheets.spreadsheets().values().get(spreadsheetId=sheet_id, range=sheet_name).execute()

        output_file = local_file_name
        with open(output_file, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f, delimiter='\t', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
            res = result.get('values')
            if res:
                writer.writerows(res)
            self.log(F"Saved to {output_file}")
        f.close()
        self.log(F"Done.")
