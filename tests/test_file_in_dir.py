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


# проверка существования элемента
# def check_exists_by_xpath(xpath, driver):
#     try:
#         block_sch = driver.find_element(By.CSS_SELECTOR, xpath)
#     except NoSuchElementException:
#         return False
#     return True


# # чтение файла
# def read_file(path):
#     try:
#         for f in os.listdir(path):
#             if f.endswith(".pdf"):
#                 fl = open(f)
#                 fl.close()
#     except FileNotFoundError:
#         return False
#     return True


# # удаление файлов
# def remove_folder(path):
#     for f in os.listdir(path):
#         if f.endswith(".pdf"):
#             os.remove(f)

def file_in_dir(path):
    list_dir = glob.glob(path)
        for f in list_dir:
#    for f in os.listdir(path):
#        if f.endswith(".pdf"):
           glob.glob("/*.pdf")
           return True
       return False

# проверка существования элемента
def check_exists_by_xpath(xpath, driver):
    try:
        block_sch = driver.find_element(By.CSS_SELECTOR, xpath)
    except NoSuchElementException:
        return False
    return True


# чтение файла
def read_file(path):
    try:
        list_dir = glob.glob(path)
        for f in list_dir:
            fl = open(f)
            fl.close()
    except FileNotFoundError:
        return False
    return True


class TestReceipts():
    # скачивание квитанции (существование файла в папке загрузок)
    def test_download_file(self, config):
        assert file_in_dir(f"{config['path_to_download']}/*.pdf")

    # является ли файл доступным и читаемым
    def test_read_file(self, config):
        assert read_file(f"{config['path_to_download']}/*.pdf")
