import pytest
import time
from datetime import datetime
import json
import os.path
import glob
import allure
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from allure_commons.types import AttachmentType
from selenium.webdriver.common.action_chains import ActionChains


# # чтение файла
# def read_file(path):
#     os.chdir(path)
#     for file in glob.glob("*.pdf"):
#         fl = open(file)
#         fl.close()
#         return True
#     return False

def file_in_dir(path):
    dir = os.path.abspath(os.curdir)
    os.chdir(dir)
    for file in glob.glob(path):
        print(file)
        return True
    return False


class TestReceipts():
    # скачивание квитанции (существование файла в папке загрузок)
    def test_download_file(self, config):
        assert file_in_dir(f"*.pdf")

#     # является ли файл доступным и читаемым
#     def test_read_file(self, config):
#         assert read_file(f"{config['path_to_download']}")
