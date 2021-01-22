import pytest
import time
import allure
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


# проверка существования элемента
def check_exists_by_xpath(xpath, driver):
    try:
        WebDriverWait(driver, 5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, xpath)))
        block_sch = driver.find_element(By.CSS_SELECTOR, xpath)
    except NoSuchElementException:
        return False
    return True


# Меню - Главная
class TestMenuMain():
    # Переход на страницу оплаты при нажатии на сумму оплаты в navbar
    def test_sum_pay(self, config, driver, login_lk):
        driver.get(f"{config['link']}/{config['account']['base_code']}/account/{config['account']['ls']}")
        sum_pay = driver.find_element(By.CSS_SELECTOR, ".widget-section3 a")
        sum_pay.click()

        assert str(driver.current_url) == \
               f"{config['link']}/{config['account']['base_code']}/account/{config['account']['ls']}/payment"

    # Переход на страницу Обращения
    def test_appeals_button(self, config, driver, login_lk):
        driver.get(f"{config['link']}/{config['account']['base_code']}/account/{config['account']['ls']}")
        button = driver.find_element(By.CSS_SELECTOR, "._appeals_content .btn")
        button.click()

        url_appeals = driver.current_url

        assert url_appeals == f"{config['link']}/" \
                              f"{config['account']['base_code']}/account/{config['account']['ls']}/appeals"








