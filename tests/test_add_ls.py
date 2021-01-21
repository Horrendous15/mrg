import pytest
import time
import json
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
        block = driver.find_element(By.CSS_SELECTOR, xpath)
    except NoSuchElementException:
        return False
    return True


# Управление
class TestAddAccount():
    # Сообщение о неверно введенных данных
    def test_invalid_ls(self, config, driver, login_lk):
        driver.get(f"{config['link']}/{config['account']['base_code']}/account/{config['account']['ls']}/add")
        try:
            WebDriverWait(driver, 3).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR,
                                                                                   ".widget-bind-ls")))
            input_ls = driver.find_element(By.CSS_SELECTOR, "#account")
            input_ls.send_keys("1")

            input_fio = driver.find_element(By.CSS_SELECTOR, "#full_name")
            input_fio.send_keys("1")

            input_sum = driver.find_element(By.CSS_SELECTOR, "#summ")
            input_sum.send_keys("1")

            button = driver.find_element(By.CSS_SELECTOR, "#bindnewls .submit-buttons .btn")
            button.click()

            assert (check_exists_by_xpath(".stack-alert", driver)) & \
                   (driver.find_element(By.CSS_SELECTOR, ".stack-alert").text ==
                    "Ошибка привязки лицевого счета. Укажите корректный номер ЛС и/или сумму")

        except TimeoutException:
            assert check_exists_by_xpath(".widget-bind-ls", driver)

    # Переход на страницу Обращения
    def test_appeals_button(self, config, driver, login_lk):
        driver.get(f"{config['link']}/{config['account']['base_code']}/account/{config['account']['ls']}/add")
        try:
            WebDriverWait(driver, 3).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR,
                                                                                   ".widget-bind-ls")))
            button = driver.find_element(By.CSS_SELECTOR, "._appeals_content .btn")
            button.click()

            url_appeals = driver.current_url

            assert url_appeals == f"{config['link']}/" \
                                  f"{config['account']['base_code']}/account/{config['account']['ls']}/appeals"

        except TimeoutException:
            assert check_exists_by_xpath(".widget-bind-ls", driver)

    # список лицевых счетов (navbar и таблица)
    def test_list_ls(self, config, driver, login_lk):
        driver.get(f"{config['link']}/{config['account']['base_code']}/account/{config['account']['ls']}/add")
        try:
            WebDriverWait(driver, 3).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR,
                                                                                  ".widget-bind-ls")))
            navbar_select_ls = driver.find_element(By.CSS_SELECTOR, "#select_ls_link")
            navbar_select_ls.click()

            time.sleep(1)

            list_ls_navbar = driver.find_elements(By.CSS_SELECTOR, ".dropdown-menu-right1.show a span:nth-child(1)")
            list_ls = [el.text for el in list_ls_navbar]

            list_ls_table = driver.find_elements(By.CSS_SELECTOR, "#sch-values tbody tr td:nth-child(2)")
            list_add_ls = [el.text for el in list_ls_table]

            assert list_ls == list_add_ls

        except TimeoutException:
            assert check_exists_by_xpath(".widget-bind-ls", driver)
