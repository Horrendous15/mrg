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


# удаление файлов
def remove_folder(path):
    list_dir = glob.glob(path)
    for f in list_dir:
        os.remove(f)


class TestReceipts():
    # скачивание квитанции (существование файла в папке загрузок)
    def test_download_file(self, config, driver, login_lk):
        driver.get(f"{config['link']}/{config['account']['base_code']}/account/{config['account']['ls']}/receipts")

        try:
            WebDriverWait(driver, 5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR,
                                                                                  ".col-12.widget-receipts-history")))
            remove_folder(f"{config['path_to_download']}\\*.pdf")

            download_click = driver.find_element(By.CSS_SELECTOR, "tr:nth-child(1) .getReceipt")

            download_click.click()

        except TimeoutException:
            assert check_exists_by_xpath(".col-12.widget-receipts-history", driver)

    # является ли файл доступным и читаемым
    def test_read_file(self, config, driver, login_lk):
        driver.get(f"{config['link']}/{config['account']['base_code']}/account/{config['account']['ls']}/receipts")
        try:
            WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR,
                                                                                   ".col-12.widget-receipts-history")))
            remove_folder(f"{config['path_to_download']}\\*.pdf")

            download_click = driver.find_element(By.CSS_SELECTOR, "tr:nth-child(1) .getReceipt")
            download_click.click()

        except TimeoutException:
            assert check_exists_by_xpath(".col-12.widget-receipts-history", driver)