import pytest
import time
import json
import allure
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException


# проверка существования элемента
def check_exists_by_xpath(xpath, driver):
    try:
        block_sch = driver.find_element(By.CSS_SELECTOR, xpath)
    except NoSuchElementException:
        return False
    return True


# Обращения
class TestMenuAppeals():
    # Предупреждение о незаполненных полях
    def test_warning(self, config, driver, login_lk):
        driver.get(f"{config['link']}/{config['account']['base_code']}/account/{config['account']['ls']}/appeals")
        try:
            WebDriverWait(driver, 5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR,
                                                                                   ".col-12.appeals-tabs")))
            themes = driver.find_element(By.CSS_SELECTOR, "#appealTheme")
            themes.send_keys("Прочие")

            button = driver.find_element(By.CSS_SELECTOR, "#appealform .btn")
            button.click()

            assert (check_exists_by_xpath("#appeal .alert", driver)) & \
                   (driver.find_element(By.CSS_SELECTOR, "#appeal .alert").text == "Не все поля заполнены")
        except TimeoutException:
            assert check_exists_by_xpath(".col-12.appeals-tabs", driver)
