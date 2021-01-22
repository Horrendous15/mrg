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

# pytest test_welcome.py --alluredir result


# проверка существования элемента
def check_exists_by_xpath(xpath, driver):
    try:
        WebDriverWait(driver, 5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, xpath)))
        block_sch = driver.find_element(By.CSS_SELECTOR, xpath)
    except Exception:
        return False
    return True


# Тестирование окна авторизации и регистрации
class TestWelcome():
    # Авторизация с неверным паролем
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

    # Регистрация с уже зарегестрированной почтой
    def test_invalid_registration(self, config, driver):

        driver.get(f"{config['link']}")

        registration = driver.find_element(By.CSS_SELECTOR, "#authorization .text-right h3")
        registration.click()

        time.sleep(1)
        slider_reg = driver.find_element(By.ID, "registration")
        if slider_reg.is_displayed():
            login_input = driver.find_element(By.CSS_SELECTOR, "#registration_form .row:nth-child(2) .form-control")
            login_input.send_keys("web@stack-it.ru")

            pass_input = driver.find_element(By.CSS_SELECTOR, "#registration_form .row:nth-child(3) .form-control")
            pass_input.send_keys(f"123456Qwe")

            checkbox = driver.find_element(By.CSS_SELECTOR, "#personal_data")
            checkbox.click()

            button = driver.find_element(By.CSS_SELECTOR, "#registration_form .btn")
            button.click()

            error_text = driver.find_element(By.CSS_SELECTOR, ".error").text

            assert error_text == "Вы были зарегистрированы ранее"
        else:
            print("Registration not is displayed")

    # Восстановление пароля с незарегестрированной почтой
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

    # Возвращение на окно авторизации из окна Восстановления пароля
    def test_back_authorization(self, config, driver):
        driver.get(f"{config['link']}")

        recover_link = driver.find_element(By.CSS_SELECTOR, "#recover_password_link")
        recover_link.click()
        time.sleep(1)
        try:
            recover = driver.find_element(By.CSS_SELECTOR, "#recover_password")
            link_auth = driver.find_element(By.CSS_SELECTOR, "#recover_form .text-right a")
            link_auth.click()

            time.sleep(1)
            authorization = driver.find_element(By.ID, "authorization")
            assert authorization.is_displayed()
        except NoSuchElementException:
            assert check_exists_by_xpath("#recover_password", driver)


# Тестирование передачи данных без регистрации
class TestWithoutRegistrationSendCounters():
    # Появление формы для передачи показаний
    def test_block_send_counters(self, config, driver):
        driver.get(f"{config['link']}")

        button_counters = driver.find_element(By.CSS_SELECTOR, "#auth_slide_outer .send_counters")
        button_counters.click()

        WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".noauth-content")))

        driver.find_element(By.CSS_SELECTOR, ".dropdown-toggle").click()
        regions = driver.find_elements(By.XPATH, "//li/a[@class]")
        for item in regions:
            if item.text == f"{config['account']['region']}":
                item.click()
                ls_input = driver.find_element(By.ID, "lsNumber")
                ls_input.send_keys(f"{config['account']['ls']}")

                fio_input = driver.find_element(By.ID, "full_name")
                fio_input.send_keys(f"{config['account']['fio']}")

                button = driver.find_element(By.CSS_SELECTOR, "#sendCountersValues .btn.stack-btn-blue")
                button.click()

                assert check_exists_by_xpath("#sendCountersValues .row .block-sch:nth-child(3)", driver), \
                    "Неверные данные"
                break
        else:
            print(f"The region '{config['account']['region']}' is not in the list")

    # Подсказка для ввода фио
    @pytest.mark.parametrize("button", [".send_counters", ".noauth_pay"])
    def test_fio_info_hover(self, config, driver, button):
        driver.get(f"{config['link']}")

        button_counters = driver.find_element(By.CSS_SELECTOR, f"#auth_slide_outer {button}")
        button_counters.click()

        WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".noauth-content")))

        info = driver.find_element(By.CSS_SELECTOR, "#popover_open")
        ActionChains(driver).move_to_element(info).perform()

        assert check_exists_by_xpath(".popover.show", driver)


# Тестирование оплаты без регистрации
class TestWithoutRegistrationPay():
    # Появление формы для передачи показаний
    def test_block_pay(self, config, driver):
        driver.get(f"{config['link']}")

        button_pay = driver.find_element(By.CSS_SELECTOR, "#auth_slide_outer .noauth_pay")
        button_pay.click()

        WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".noauth-content")))

        driver.find_element(By.CSS_SELECTOR, ".dropdown-toggle").click()
        regions = driver.find_elements(By.XPATH, "//li/a[@class]")
        for item in regions:
            if item.text == f"{config['account']['region']}":
                item.click()
                ls_input = driver.find_element(By.ID, "lsNumber")
                ls_input.send_keys(f"{config['account']['ls']}")

                fio_input = driver.find_element(By.ID, "full_name")
                fio_input.send_keys(f"{config['account']['fio']}")

                button = driver.find_element(By.ID, "checkLS")
                button.click()
                time.sleep(1)
                assert (check_exists_by_xpath("#container .row.kvt", driver)
                        & check_exists_by_xpath("#container .row.banks-block", driver)),\
                    "Неверные данные"
                break
        else:
            print(f"The region '{config['account']['region']}' is not in the list")
