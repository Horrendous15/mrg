import pytest
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait


class TestWelcome():

    def test_invalid_pass(self, config, driver):

        driver.get(f"{config['link']}")

        login_input = driver.find_element(By.CSS_SELECTOR, "#authorization_form .form-group:nth-child(2) .form-control")
        login_input.send_keys(f"{config['login_auth']}")

        pass_input = driver.find_element(By.CSS_SELECTOR, "#authorization_form .form-group:nth-child(3) .form-control")
        pass_input.send_keys(f"{config['invalid_pass']}")

        button = driver.find_element(By.CSS_SELECTOR, "#authorization_form .btn")
        button.click()

        error_text = driver.find_element(By.CSS_SELECTOR, ".error").text

        assert error_text == "Ошибка авторизации"

    def test_invalid_registration(self, config, driver):

        driver.get(f"{config['link']}")

        registration = driver.find_element(By.CSS_SELECTOR, "#authorization .text-right h3")
        registration.click()

        time.sleep(1)
        slider_reg = driver.find_element(By.ID, "registration")
        if slider_reg.is_displayed():
            login_input = driver.find_element(By.CSS_SELECTOR, "#registration_form .row:nth-child(2) .form-control")
            login_input.send_keys("2@ru")

            pass_input = driver.find_element(By.CSS_SELECTOR, "#registration_form .row:nth-child(3) .form-control")
            pass_input.send_keys(f"{config['password_reg']}")

            checkbox = driver.find_element(By.CSS_SELECTOR, "#personal_data")
            checkbox.click()

            button = driver.find_element(By.CSS_SELECTOR, "#registration_form .btn")
            button.click()

            error_text = driver.find_element(By.CSS_SELECTOR, ".error").text

            assert error_text == "Вы были зарегистрированы ранее"
        else:
            print("Registration not is displayed")

    def test_recover_invalid_email(self, config, driver):
        driver.get(f"{config['link']}")

        recover_link = driver.find_element(By.CSS_SELECTOR, "#recover_password_link")
        recover_link.click()
        time.sleep(1)
        registration = driver.find_element(By.CSS_SELECTOR, "#recover_password")
        if registration.is_displayed():
            registration_input = driver.find_element(By.CSS_SELECTOR, "#recover_password .form-control")
            registration_input.send_keys("12@12")

            button = driver.find_element(By.CSS_SELECTOR, "#recover_password .btn")
            button.click()
            error_text = driver.find_element(By.CSS_SELECTOR, ".error").text
            assert error_text == "Указаный e-mail не зарегистрирован"
        else:
            print("Recover password not is displayed")

    def test_back_authorization(self, config, driver):
        driver.get(f"{config['link']}")

        recover_link = driver.find_element(By.CSS_SELECTOR, "#recover_password_link")
        recover_link.click()
        time.sleep(1)
        recover = driver.find_element(By.CSS_SELECTOR, "#recover_password")
        if recover.is_displayed():
            link_auth = driver.find_element(By.CSS_SELECTOR, "#recover_form .text-right a")
            link_auth.click()

            time.sleep(1)
            authorization = driver.find_element(By.ID, "authorization")
            assert authorization.is_displayed()
        else:
            print("Recover password not is displayed")


class TestWithoutRegistration():
    def test_send_counters(self, config, driver):
        driver.get(f"{config['link']}")

        button_counters = driver.find_element(By.CSS_SELECTOR, "#auth_slide_outer .send_counters")
        button_counters.click()

        WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".noauth-content")))

        driver.find_element(By.CSS_SELECTOR, ".dropdown-toggle").click()
        first_region = driver.find_element(By.CSS_SELECTOR, "#bs-select-1  li:nth-child(1) .dropdown-item")
        first_region.click()

        ls_input = driver.find_element(By.ID, "lsNumber")
        ls_input.send_keys(f"{config['ls']}")

        fio_input = driver.find_element(By.ID, "full_name")
        fio_input.send_keys(f"{config['fio']}")
        time.sleep(3)