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


class TestNavbar():
    # Переход на страницу оплаты при нажатии на сумму оплаты в navbar
    def test_sum_pay(self, login_lk, driver, config):
        sum_pay = driver.find_element(By.CSS_SELECTOR, ".pay-second")
        sum_pay.click()

        assert str(driver.current_url) == \
               f"{config['link']}/{config['account']['base_code']}/account/{config['account']['ls']}/payment"

    # переход на страницу добавления лс
    def test_add_ls(self, login_lk, driver, config):

        navbar_select_ls = driver.find_element(By.CSS_SELECTOR, "#select_ls_link")
        navbar_select_ls.click()

        time.sleep(1)

        list_ls_navbar = driver.find_elements(By.CSS_SELECTOR, ".dropdown-menu-right1.show a")
        add_ls = list_ls_navbar[-3]
        add_ls.click()

        url_add_ls = driver.current_url

        assert url_add_ls == \
               f"{config['link']}/{config['account']['base_code']}/account/{config['account']['ls']}/add"

    # переход на страницу настроек
    def test_add_settings(self, login_lk, driver, config):

        navbar_select_ls = driver.find_element(By.CSS_SELECTOR, "#select_ls_link")
        navbar_select_ls.click()

        time.sleep(1)

        list_ls_navbar = driver.find_elements(By.CSS_SELECTOR, ".dropdown-menu-right1.show a")
        settings = list_ls_navbar[-2]
        settings.click()

        url_settings = driver.current_url

        assert url_settings == \
               f"{config['link']}/{config['account']['base_code']}/account/{config['account']['ls']}/profile"

    # Выход из лк
    def test_logout(self, login_lk, driver, config):
        navbar_select_ls = driver.find_element(By.CSS_SELECTOR, "#select_ls_link")
        navbar_select_ls.click()

        time.sleep(1)

        list_ls_navbar = driver.find_elements(By.CSS_SELECTOR, ".dropdown-menu-right1.show a")
        logout_click = list_ls_navbar[-1]
        logout_click.click()

        url_logout = driver.current_url

        assert url_logout == f"{config['link']}/login"