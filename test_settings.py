import pytest
import time
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


# существование элемента в списке
def select_elem(list_el, string):
    if string in list_el:
        return True
    return False


class TestMenuProfile():
    # добавление номера телефона
    def test_add_phone_number(self, config, driver, login_lk):
        driver.get(f"{config['link']}/{config['account']['base_code']}/account/{config['account']['ls']}/profile")
        try:
            WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR,
                                                                                   ".widget-profile")))

            subscription = driver.find_element(By.CSS_SELECTOR, "#archive-tab")
            subscription.click()

            add_phone = driver.find_element(By.CSS_SELECTOR, ".add-phone-label")
            add_phone.click()

            phone = "1211211111"

            input_phone = driver.find_element(By.CSS_SELECTOR, "#phoneNumberNew")
            input_phone.send_keys(phone)

            button_save = driver.find_element(By.CSS_SELECTOR, '#addPhoneSave')
            button_save.click()

            time.sleep(2)

            list_phone = driver.find_elements(By.CSS_SELECTOR, "#subscriptions .phone-row .phone")
            list_phone = [el.text for el in list_phone]

            number_phone = "8"+phone
            assert select_elem(list_phone, number_phone)

        except TimeoutException:
            assert check_exists_by_xpath(".col-12.widget-receipts-history", driver)

    # редактирование номера телефона
    def test_edit_phone_number(self, config, driver, login_lk):
        driver.get(f"{config['link']}/{config['account']['base_code']}/account/{config['account']['ls']}/profile")
        try:
            WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR,
                                                                                   ".widget-profile")))

            subscription = driver.find_element(By.CSS_SELECTOR, "#archive-tab")
            subscription.click()

            phone = "81211211111"

            list_phone = driver.find_elements(By.CSS_SELECTOR, "#subscriptions .phone-row")

            for el in list_phone:
                if phone in el.text:
                    id_phone = el.get_attribute("id")
                    edit_click = driver.find_element(By.CSS_SELECTOR, f"#subscriptions #{id_phone} .mdi-pencil")
                    edit_click.click()
                    input_edit = driver.find_element(By.CSS_SELECTOR, "#phoneNumberEdit")
                    input_edit.send_keys(Keys.BACKSPACE*10)
                    input_edit.send_keys("1311311111")
                    button_save = driver.find_element(By.CSS_SELECTOR, "#editPhoneSave")
                    button_save.click()
                    break
            new_phone = "8"+"1311311111"
            time.sleep(1)
            list_phone = driver.find_elements(By.CSS_SELECTOR, "#subscriptions .phone-row .phone")
            list_phone = [el.text for el in list_phone]

            assert select_elem(list_phone, new_phone)

        except TimeoutException:
            assert check_exists_by_xpath(".col-12.widget-receipts-history", driver)

    # удаление номера телефона
    def test_delete_phone_number(self, config, driver, login_lk):
        driver.get(f"{config['link']}/{config['account']['base_code']}/account/{config['account']['ls']}/profile")
        try:
            WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR,
                                                                                   ".widget-profile")))

            subscription = driver.find_element(By.CSS_SELECTOR, "#archive-tab")
            subscription.click()

            phone = "81311311111"

            list_phone = driver.find_elements(By.CSS_SELECTOR, "#subscriptions .phone-row")

            for el in list_phone:
                if phone in el.text:
                    id_phone = el.get_attribute("id")
                    delete_click = driver.find_element(By.CSS_SELECTOR, f"#subscriptions #{id_phone} .mdi-delete")
                    delete_click.click()
                    button_save = driver.find_element(By.CSS_SELECTOR, "#removePhoneSave")
                    button_save.click()
                    break
            time.sleep(1)
            list_phone = driver.find_elements(By.CSS_SELECTOR, "#subscriptions .phone-row .phone")
            list_phone = [el.text for el in list_phone]

            assert not select_elem(list_phone, phone)

        except TimeoutException:
            assert check_exists_by_xpath(".col-12.widget-receipts-history", driver)