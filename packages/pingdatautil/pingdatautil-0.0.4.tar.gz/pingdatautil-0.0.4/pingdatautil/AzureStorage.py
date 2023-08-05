# -*- coding: utf-8 -*-

import os
import sys
import time
from datetime import datetime
from azure.identity import ClientSecretCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, ContentSettings


class AzureStorage():
    def __init__(self, logger=None):
        self.blob_service_client = None
        self.container_client = None
        self.logger = None
        if logger:
            self.logger = logger

    def log(self, input_str, level=None):
        ident = "[AZ-STORAGE] "
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

    def blob_connect_by_sas(self, account_url, container, sas_token):
        self.blob_service_client = BlobServiceClient(account_url=account_url, credential=sas_token)
        self.log(F"Connect using SAS Token to account {account_url}")
        try:
            self.container_client = self.blob_service_client.get_container_client(container=container)
            self.log(F"Connect to Container {container}")
        except Exception as e:
            print(str(e))

    def blob_connect_by_credential(self, account_url, container, tenant_id, client_id, client_secret):
        self.blob_service_client = BlobServiceClient
        csc = ClientSecretCredential(tenant_id, client_id, client_secret)
        self.blob_service_client = BlobServiceClient(account_url=account_url, credential=csc)
        self.log(F"Connect using credential to account {account_url}")
        try:
            self.container_client = self.blob_service_client.get_container_client(container=container)
            self.log(F"Connect to Container {container}")
        except Exception as e:
            print(str(e))

    def list_blob_prefix(self, path):
        self.log(F"Querying Blob in {path}")
        list_blob_output = None
        try:
            list_blob = self.container_client.list_blobs(path)
            list_blob_output = []
            total_blob = 0
            for i, blob in enumerate(list_blob):
                total_blob = i + 1
                if (total_blob % 1000 == 0):
                    self.log(F"{str(total_blob)} blobs read")
                list_blob_output.append(blob.name)
            self.log(F"{str(total_blob)} blobs read")
        except Exception as e:
            self.log(str(e), "ERROR")
        list_blob_output = sorted(list_blob_output)
        return list_blob_output

    def upload(self, local_file_name, target_file_name=None):
        if not target_file_name:
            target_file_name = os.path.basename(local_file_name)
        blob_client = self.container_client.get_blob_client(target_file_name)
        with open(local_file_name, "rb") as data:
            self.log(F"Upload : {local_file_name}")
            blob_client.upload_blob(data, overwrite=True)
            self.log(F"Uploaded to : {target_file_name}")

    def upload_text(self, local_file_name, target_file_name=None):
        if not target_file_name:
            target_file_name = os.path.basename(local_file_name)
        blob_client = self.container_client.get_blob_client(target_file_name)

        with open(local_file_name, "rb") as data:
            self.log(F"Upload : {local_file_name}")
            content_settings = ContentSettings(content_type='text/plain')
            blob_client.upload_blob(data, overwrite=True, content_settings=content_settings)
            self.log(F"Uploaded to : {target_file_name}")

    def delete(self, target_file_name):
        try:
            self.container_client.delete_blob(blob=target_file_name)
            self.log(F"Delete file : " + target_file_name)
        except Exception as e:
            self.log(str(e), "ERROR")

    def upload_recursive(self, local_root_path, target_root_path):
        path_remove = local_root_path
        for r, d, f in os.walk(local_root_path):
            if f:
                for local_file in f:
                    target_file_name = target_root_path + "/" + os.path.join(r, local_file).replace(path_remove,
                                                                                                    "").replace("\\",
                                                                                                                "/")
                    local_file_name = os.path.join(r, local_file).replace("\\", "/")
                    with open(local_file_name, "rb") as data:
                        self.log(F"Upload : {local_file_name}")
                        blob_client = self.container_client.get_blob_client(target_file_name)
                        blob_client.upload_blob(data, overwrite=True)
                        self.log(F"Uploaded to : {target_file_name}")

    def list_local_path(self, path):
        self.log(F"Querying local path in {path}")
        list_immediate_path = next(os.walk(path))[1]
        print(list_immediate_path)

    def delete_list_of_path(self, prefix, list_delete_path):
        list_of_path = self.list_blob_prefix(prefix)
        list_of_path.sort(reverse=True, key=len)
        list_to_delete = []
        for path in list_of_path:
            for delete_path in list_delete_path:
                if path.startswith(prefix + "/" + delete_path):
                    list_to_delete.append(path)
        self.log("Will delete " + str(list_to_delete))
        for path in list_to_delete:
            self.delete(path)

    '''
    def delete_folder(containername, foldername):
        folders = [blob.name for blob in blob_client.list_blobs(containername, prefix=foldername)]
        folders.sort(reverse=True, key=len)
        if len(folders) > 0:
            for folder in folders:
                blob_client.delete_blob(containername, folder)
                print("deleted folder", folder)
    '''

    def delete_folder(self, folder):
        bloblistingresult = self.container_client.list_blobs(container_name='container-name', delimiter='/')
        for i in bloblistingresult.prefixes:
            print(i.name)

    def download(self, target_file_name, local_file_name):
        self.log(F"Downloading : " + target_file_name)
        self.log(F"Save to : " + local_file_name)
        blob_client = self.container_client.get_blob_client(target_file_name)
        with open(local_file_name, "wb") as data:
            data.write(blob_client.download_blob().readall())

