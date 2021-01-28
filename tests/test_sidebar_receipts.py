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
        for f in os.listdir(path):
            if f.endswith(".pdf"):
                fl = open(f)
                fl.close()
    except FileNotFoundError:
        return False
    return True


# удаление файлов
def remove_folder(path):
    for f in os.listdir(path):
        if f.endswith(".pdf"):
            os.remove(f)


def file_in_dir(path):
    for f in os.listdir(path):
        if f.endswith(".pdf"):
            os.path.join(path, f)
            return True
        return False


# квитанции
class TestMenuReceipts():
    # Вывод данных за указанный год
    def test_data_for_year(self,  config, driver, login_lk):
        driver.get(f"{config['link']}/{config['account']['base_code']}/account/{config['account']['ls']}/receipts")
        try:
            WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR,
                                                                                   ".col-12.widget-receipts-history")))

            select_year = driver.find_element(By.CSS_SELECTOR, "#receipts_year").get_attribute("value")

            year = datetime.strptime(select_year, "%Y")

            dates_list = driver.find_elements(By.CSS_SELECTOR, "#receiptsTable td span")
            for el in dates_list:
                element = datetime.strptime(el.get_attribute("data-sort"), "%d.%m.%y")
                assert year.year == element.year

        except TimeoutException:
            assert check_exists_by_xpath(".col-12.widget-receipts-history", driver)

    # Детализация начислений: появление окна
    def test_details_accruals(self, config, driver, login_lk):
        driver.get(f"{config['link']}/{config['account']['base_code']}/account/{config['account']['ls']}/receipts")
        try:
            WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR,
                                                                                   ".col-12.widget-receipts-history")))

            show_details = driver.find_element(By.CSS_SELECTOR, ".showDetalizationModal")
            show_details.click()

            assert check_exists_by_xpath(".modal.show", driver), \
                allure.attach(driver.get_screenshot_as_png(), name='screenshot', attachment_type=AttachmentType.PNG)

        except TimeoutException:
            assert check_exists_by_xpath(".col-12.widget-receipts-history", driver)

    # Детализация начислений: сортировка
    @pytest.mark.parametrize("number_column", ["2", "3", "4", "5", "6", "7", "8", "9"],
                             ids=["Тариф", "Входящее сальдо", "Начислено",
                                  "Перерасчет", "Снято", "Платежи", "Исходящее сальдо", "Объем"])
    def test_details_accruals_sort(self, config, driver, login_lk, number_column):
        driver.get(f"{config['link']}/{config['account']['base_code']}/account/{config['account']['ls']}/receipts")
        try:
            WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR,
                                                                                   ".col-12.widget-receipts-history")))

            show_details = driver.find_element(By.CSS_SELECTOR, ".showDetalizationModal")
            show_details.click()

            time.sleep(2)

            list_elem = driver.find_elements(By.CSS_SELECTOR,
                                             f"#accrualsDetalizationTable tbody td:nth-child({number_column})")
            list_sort_exp = [item.text.replace(" ", "") for item in list_elem]
            list_sort_exp.sort(key=float)

            sort_click = driver.find_element(By.CSS_SELECTOR,
                                             f"#accrualsDetalizationTable thead th:nth-child({number_column})")
            sort_click.click()

            actual_result = driver.find_elements(By.CSS_SELECTOR,
                                                 f"#accrualsDetalizationTable tbody td:nth-child({number_column})")
            list_sort_actual = [el.text.replace(" ", "") for el in actual_result]

            assert list_sort_exp == list_sort_actual, \
                allure.attach(driver.get_screenshot_as_png(), name='screenshot', attachment_type=AttachmentType.PNG)

        except TimeoutException:
            assert check_exists_by_xpath(".col-12.widget-receipts-history", driver)

    # Сортировка
    @pytest.mark.parametrize("number_column", ["2", "3"])
    def test_receipts_sort(self, config, driver, login_lk, number_column):
        driver.get(f"{config['link']}/{config['account']['base_code']}/account/{config['account']['ls']}/receipts")
        try:
            WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR,
                                                                                   ".col-12.widget-receipts-history")))

            list_elem = driver.find_elements(By.CSS_SELECTOR,
                                             f"#receiptsTable tbody td:nth-child({number_column})")
            list_sort_exp = [item.text.replace(" ", "") for item in list_elem]
            list_sort_exp.sort(key=float)

            sort_click = driver.find_element(By.CSS_SELECTOR,
                                             f"#receiptsTable thead th:nth-child({number_column})")
            sort_click.click()

            actual_result = driver.find_elements(By.CSS_SELECTOR,
                                                 f"#receiptsTable tbody td:nth-child({number_column})")
            list_sort_actual = [el.text.replace(" ", "") for el in actual_result]

            assert list_sort_exp == list_sort_actual, \
                allure.attach(driver.get_screenshot_as_png(), name='screenshot', attachment_type=AttachmentType.PNG)

        except TimeoutException:
            assert check_exists_by_xpath(".col-12.widget-receipts-history", driver)

    # скачивание квитанции (существование файла в папке загрузок)
    def test_download_file(self, config, driver, login_lk):
        driver.get(f"{config['link']}/{config['account']['base_code']}/account/{config['account']['ls']}/receipts")

        try:
            WebDriverWait(driver, 5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR,
                                                                                  ".col-12.widget-receipts-history")))
            remove_folder(f"{config['path_to_download']}")

            download_click = driver.find_element(By.CSS_SELECTOR, "tr:nth-child(1) .getReceipt")

            download_click.click()
            time.sleep(2)

            assert file_in_dir(f"{config['path_to_download']}")
        except TimeoutException:
            assert check_exists_by_xpath(".col-12.widget-receipts-history", driver)

    # является ли файл доступным и читаемым
    def test_read_file(self, config, driver, login_lk):
        driver.get(f"{config['link']}/{config['account']['base_code']}/account/{config['account']['ls']}/receipts")
        try:
            WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR,
                                                                                   ".col-12.widget-receipts-history")))
            remove_folder(f"{config['path_to_download']}")

            download_click = driver.find_element(By.CSS_SELECTOR, "tr:nth-child(1) .getReceipt")
            download_click.click()
            time.sleep(3)

            assert read_file(f"{config['path_to_download']}")

        except TimeoutException:
            assert check_exists_by_xpath(".col-12.widget-receipts-history", driver)


