import pytest
import time
from datetime import datetime
import json
import allure
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys


# проверка существования элемента
def check_exists_by_xpath(xpath, driver):
    try:
        block_sch = driver.find_element(By.CSS_SELECTOR, xpath)
    except NoSuchElementException:
        return False
    return True


# Меню - Оплата
class TestMenuPayment():
    # Ввод данных и подсчет общей суммы оплаты
    def test_enter_values(self, config, driver, login_lk):
        driver.get(f"{config['link']}/{config['account']['base_code']}/account/{config['account']['ls']}/payment")
        try:
            sum_s = 1.02
            sum_p = 0.01
            sum_result = (str(sum_s+sum_p).replace('.', ','))

            sum_services = driver.find_element(By.CSS_SELECTOR, '.col-12.col-md-4:nth-child(1) input')
            sum_services.send_keys(Keys.BACKSPACE*10)
            sum_services.send_keys(f"{sum_s}")

            sum_peni = driver.find_element(By.CSS_SELECTOR, ".col-12.col-md-4:nth-child(2) input")
            sum_peni.send_keys(Keys.BACKSPACE*10)
            sum_peni.send_keys(f"{sum_p}")

            general_sum = driver.find_element(By.CSS_SELECTOR, ".col-12.col-md-4:nth-child(3) .pay_row_summ")
            sum_paid = driver.find_element(By.CSS_SELECTOR, "#pay_amount")
            assert (general_sum.get_attribute("value") == sum_result) & (sum_paid.get_attribute("value") == sum_result)
        except TimeoutException:
            assert check_exists_by_xpath(".col-12.widget-big", driver)

    # Перечень услуг в блоке ввода данных
    def test_list_services(self, config, driver, login_lk):
        driver.get(f"{config['link']}/{config['account']['base_code']}/account/{config['account']['ls']}/payment")
        try:
            WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".col-12.widget-big")))

            driver.find_element(By.CSS_SELECTOR, ".kvt-title.mb-0").click()

            assert check_exists_by_xpath(".collapse.show", driver)

        except TimeoutException:
            assert check_exists_by_xpath(".col-12.widget-big", driver)

    # Информация "Безопасность платежей"
    def test_popover_info(self, config, driver, login_lk):
        driver.get(f"{config['link']}/{config['account']['base_code']}/account/{config['account']['ls']}/payment")
        try:
            WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".col-12.widget-big")))

            driver.find_element(By.ID, "popover_open").click()

            assert check_exists_by_xpath(".bs-popover-top.show", driver)

        except TimeoutException:
            assert check_exists_by_xpath(".col-12.widget-big", driver)
