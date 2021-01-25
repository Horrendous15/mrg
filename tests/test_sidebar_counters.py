import pytest
import time
from datetime import datetime
import json
import math
import requests
import os.path
import glob
import allure
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from allure_commons.types import AttachmentType


# проверка существования элемента
def check_exists_by_xpath(xpath, driver):
    try:
        block_sch = driver.find_element(By.CSS_SELECTOR, xpath)
    except NoSuchElementException:
        return False
    return True


# Меню - Показания
class TestMenuCounters():
    # Ввод показаний и проверка вычисления расхода и суммы к оплате
    def test_enter_counters(self, config, driver, login_lk):
        driver.get(f"{config['link']}/{config['account']['base_code']}/account/{config['account']['ls']}/counters")
        try:
            WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".col-12.widget-big")))

            rate = driver.find_element(By.CSS_SELECTOR, ".block-note b:nth-child(4)").text

            rate_float = round(float(rate) * 5, 2)

            last_indications = driver.find_element(By.CSS_SELECTOR,
                                                   "#counterHistoryTable .odd:nth-child(1) td:nth-child(3)").text

            enter = driver.find_element(By.CSS_SELECTOR, ".stack-large-input")
            enter.send_keys(str(int(last_indications)+5))

            diff_indications = driver.find_element(By.CSS_SELECTOR, "._rate span").text
            pay_sch = driver.find_element(By.CSS_SELECTOR, "._pay span").text

            assert (diff_indications == str(5)) & \
                   (float(pay_sch.split()[0]) == rate_float)

        except TimeoutException:
            assert check_exists_by_xpath(".col-12.widget-big", driver)

    # Сортировка по столбцам: Счетчик, Источник
    @pytest.mark.parametrize("number_column", ["1", "5"])
    def test_sort_counter(self, config, driver, login_lk, number_column):
        driver.get(f"{config['link']}/{config['account']['base_code']}/account/{config['account']['ls']}/counters")
        try:
            WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".col-12.widget-big")))

            list_pages = driver.find_element(By.CSS_SELECTOR, "#counterHistoryTable_length")
            list_pages.click()
            list_pages.find_element(By.CSS_SELECTOR, "option:nth-child(4)").click()

            list_elem = driver.find_elements(By.CSS_SELECTOR, f"#counterHistoryTable tbody td:nth-child({number_column})")
            list_elem = [item.text for item in list_elem]
            list_sort_exp = sorted(list_elem)

            sort_click = driver.find_element(By.CSS_SELECTOR, f"#counterHistoryTable th:nth-child({number_column})")
            sort_click.click()

            actual_result = driver.find_elements(By.CSS_SELECTOR, f"#counterHistoryTable tbody td:nth-child({number_column})")
            list_sort_actual = [el.text for el in actual_result]

            assert list_sort_exp == list_sort_actual

        except TimeoutException:
            assert check_exists_by_xpath(".col-12.widget-big", driver) & \
                   check_exists_by_xpath(f"#counterHistoryTable tbody td:nth-child({number_column})", driver)

    # Сортировка по столбцам: Дата
    def test_sort_date(self, config, driver, login_lk):
        driver.get(f"{config['link']}/{config['account']['base_code']}/account/{config['account']['ls']}/counters")
        try:
            WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".col-12.widget-big")))

            list_pages = driver.find_element(By.CSS_SELECTOR, "#counterHistoryTable_length")
            list_pages.click()
            list_pages.find_element(By.CSS_SELECTOR, "option:nth-child(4)").click()

            list_elem = driver.find_elements(By.CSS_SELECTOR, "#counterHistoryTable tbody td:nth-child(2) span")
            list_sort_exp = [item.text for item in list_elem]
            list_sort_exp.sort(key=lambda date: datetime.strptime(date, "%d.%m.%y"))

            sort_click = driver.find_element(By.CSS_SELECTOR, "#counterHistoryTable .sorting:nth-child(2)")

            sort_click.click()
            actual_result = driver.find_elements(By.CSS_SELECTOR, "#counterHistoryTable tbody td:nth-child(2) span")
            list_sort_actual = [el.text for el in actual_result]

            assert list_sort_exp == list_sort_actual

        except TimeoutException:
            assert check_exists_by_xpath(".col-12.widget-big", driver)

    # Сортировка по столбцам: Показание, Расход
    @pytest.mark.parametrize("number_column", ["3", "4"])
    def test_sort_rate(self, config, driver, login_lk, number_column):
        driver.get(f"{config['link']}/{config['account']['base_code']}/account/{config['account']['ls']}/counters")
        try:
            WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".col-12.widget-big")))

            list_pages = driver.find_element(By.CSS_SELECTOR, "#counterHistoryTable_length")
            list_pages.click()
            list_pages.find_element(By.CSS_SELECTOR, "option:nth-child(4)").click()

            list_elem = driver.find_elements(By.CSS_SELECTOR, f"#counterHistoryTable tbody td:nth-child({number_column})")
            list_sort_exp = [item.text for item in list_elem]
            list_sort_exp.sort(key=int)

            sort_click = driver.find_element(By.CSS_SELECTOR, f"#counterHistoryTable .sorting:nth-child({number_column})")

            sort_click.click()
            actual_result = driver.find_elements(By.CSS_SELECTOR, f"#counterHistoryTable tbody td:nth-child({number_column})")
            list_sort_actual = [el.text for el in actual_result]

            assert list_sort_exp == list_sort_actual

        except TimeoutException:
            assert check_exists_by_xpath(".col-12.widget-big", driver)

    # Передача неверных показаний
    def test_invalid_indications(self, config, driver, login_lk):

        driver.get(f"{config['link']}/{config['account']['base_code']}/account/{config['account']['ls']}/counters")
        try:
            WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".col-12.widget-big")))

            enter = driver.find_element(By.CSS_SELECTOR, ".stack-large-input")
            enter.send_keys("1")

            button = driver.find_element(By.CSS_SELECTOR, "#sendCountersValues .row-widget-next .btn")
            button.click()

            warning = driver.find_element(By.CSS_SELECTOR, ".alert-warning.stack-alert")

            assert warning.text == "Отрицательный расход/Перекрутка"

        except TimeoutException:
            assert check_exists_by_xpath(".col-12.widget-big", driver)

    # Переход на страницу Обращения
    def test_appeals(self, config, driver, login_lk):
        driver.get(f"{config['link']}/{config['account']['base_code']}/account/{config['account']['ls']}/counters")
        try:
            WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".col-12.widget-big")))

            button_appeals = driver.find_element(By.CSS_SELECTOR, "._appeals_content .btn")
            button_appeals.click()

            url_appeals = driver.current_url

            assert url_appeals == f"{config['link']}/" \
                                  f"{config['account']['base_code']}/account/{config['account']['ls']}/appeals"

        except TimeoutException:
            assert check_exists_by_xpath(".col-12.widget-big", driver)
