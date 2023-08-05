from google.cloud import storage
import os
from datetime import datetime
import time


class GoogleStorage():
    def __init__(self, json_file=None, bucket_name=None, logger=None):

        self.json_file = None
        if json_file:
            self.json_file = json_file

        self.bucket_name = None
        if bucket_name:
            self.bucket_name = bucket_name

        self.logger = None
        if logger:
            self.logger = logger

        self.client = None
        self.bucket_name = None

        if self.json_file and self.bucket_name:
            self.connect_to_gs(json_file)
            self.connect_to_bucket(bucket_name)
        elif self.json_file:
            self.connect_to_gs(json_file)
        else:
            pass

    def log(self, input_str, level=None):
        ident = "[GOOGLE-STORAGE] "
        if not self.logger:
            dt_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print("[" + dt_str + "] " + ident + input_str)
        else:
            self.logger.log(ident + input_str, level)

    def timer_start(self):
        self.time = time.time()

    def timer_stop(self):
        t = time.time()
        i = t - self.time
        txt = "{0:,.3f}".format(i)
        txt_h = time.strftime('%H:%M:%S', time.gmtime((float(txt))))
        self.log(F"Finished in {txt}s, {txt_h}")
        return txt

    def connect_to_gs(self, json_file):
        try:
            self.log("Connect to GCP using JSON file")
            self.client = storage.Client.from_service_account_json(self.json_file)
        except Exception as e:
            self.log(str(e))

    def connect_to_bucket(self, bucket_name):
        try:
            self.log(F"Selecting Bucket : {bucket_name}")
            self.bucket = self.client.get_bucket(bucket_name)
        except Exception as e:
            self.log(str(e))

    def storage_connect(self, json_file=None, bucket_name=None):
        if self.json_file and self.bucket_name:
            self.connect_to_gs(json_file)
            self.connect_to_bucket(bucket_name)
        elif self.json_file:
            self.connect_to_gs(json_file)
        else:
            self.log("No JSON / Bucket Name Provided")
            pass

    def upload(self, file_name, gs_path):
        fn = os.path.basename(file_name)
        blob = self.bucket.blob(F"{gs_path}/{fn}")
        blob.upload_from_filename(file_name)
        self.log(F"Uploaded {fn} to gs://{self.bucket_name}/{gs_path}/{fn}")
