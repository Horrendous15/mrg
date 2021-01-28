import pytest
import time
from datetime import datetime
import allure
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


# проверка существования элемента
def check_exists_by_xpath(xpath, driver):
    try:
        block_sch = driver.find_element(By.CSS_SELECTOR, xpath)
    except NoSuchElementException:
        return False
    return True


# Начисления и платежи
class TestMenuAccruals():
    # Начисления: Сортировка по Названию услуги
    def test_sort_name(self, config, driver, login_lk):
        driver.get(f"{config['link']}/{config['account']['base_code']}/account/{config['account']['ls']}/accruals")
        try:
            WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR,
                                                                                   ".col-12.widget-accruals")))

            list_elem = driver.find_elements(By.CSS_SELECTOR, f"#gazServicesTable tbody td:nth-child(1)")
            list_elem = [item.text for item in list_elem]
            list_sort_exp = sorted(list_elem)

            sort_click = driver.find_element(By.CSS_SELECTOR, f"#gazServicesTable thead th:nth-child(1)")

            sort_click.click()
            actual_result = driver.find_elements(By.CSS_SELECTOR,
                                                 f"#gazServicesTable tbody td:nth-child(1)")
            list_sort_actual = [el.text for el in actual_result]

            assert list_sort_exp == list_sort_actual

        except TimeoutException:
            assert check_exists_by_xpath(".col-12.widget-accruals", driver)

    # Начисления: Сортировка
    @pytest.mark.parametrize("number_column", ["2", "3", "4", "5", "6", "7", "8"])
    def test_sort_accruals(self, config, driver, login_lk, number_column):
        driver.get(f"{config['link']}/{config['account']['base_code']}/account/{config['account']['ls']}/accruals")
        try:
            WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR,
                                                                                   ".col-12.widget-accruals")))

            list_elem = driver.find_elements(By.CSS_SELECTOR, f"#gazServicesTable tbody td:nth-child({number_column})")
            list_sort_exp = [item.text.replace(" ", "") for item in list_elem]

            list_sort_exp.sort(key=float)

            sort_click = driver.find_element(By.CSS_SELECTOR, f"#gazServicesTable thead th:nth-child({number_column})")
            sort_click.click()

            actual_result = driver.find_elements(By.CSS_SELECTOR,
                                                 f"#gazServicesTable tbody td:nth-child({number_column})")
            list_sort_actual = [el.text.replace(" ", "") for el in actual_result]

            assert list_sort_exp == list_sort_actual

        except TimeoutException:
            assert check_exists_by_xpath(".col-12.widget-accruals", driver)

    # История начислений: Сортировка по дате
    def test_history_accruals_sort_date(self, config, driver, login_lk):
        driver.get(f"{config['link']}/{config['account']['base_code']}/account/{config['account']['ls']}/accruals")
        try:
            WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR,
                                                                                   ".col-12.widget-accruals")))

            history = driver.find_element(By.CSS_SELECTOR, "#archive-tab")
            history.click()

            list_elem = driver.find_elements(By.CSS_SELECTOR, "#accrualsHistoryTable td .showDetalizationModal")
            list_sort_exp = [item.get_attribute("data-date") for item in list_elem]
            list_sort_exp.sort(key=lambda date: datetime.strptime(date, "%d.%m.%y"))

            sort_click = driver.find_element(By.CSS_SELECTOR, "#accrualsHistoryTable thead th:nth-child(1)")

            sort_click.click()
            actual_result = driver.find_elements(By.CSS_SELECTOR, "#accrualsHistoryTable td .showDetalizationModal")
            list_sort_actual = [el.get_attribute("data-date") for el in actual_result]

            assert list_sort_exp == list_sort_actual

        except TimeoutException:
            assert check_exists_by_xpath(".col-12.widget-accruals", driver)

    # История начислений: Сортировка
    @pytest.mark.parametrize("number_column", ["2", "3", "4", "5", "6"])
    def test_history_sort_accruals(self, config, driver, login_lk, number_column):
        driver.get(f"{config['link']}/{config['account']['base_code']}/account/{config['account']['ls']}/accruals")
        try:
            WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR,
                                                                                   ".col-12.widget-accruals")))
            history = driver.find_element(By.CSS_SELECTOR, "#archive-tab")
            history.click()

            list_elem = driver.find_elements(By.CSS_SELECTOR, f"#accrualsHistoryTable tbody td:nth-child({number_column})")
            list_sort_exp = [item.text for item in list_elem]
            list_sort_exp = [item.replace(" ", "") for item in list_sort_exp]
            list_sort_exp.sort(key=float)

            sort_click = driver.find_element(By.CSS_SELECTOR, f"#accrualsHistoryTable thead th:nth-child({number_column})")
            sort_click.click()

            actual_result = driver.find_elements(By.CSS_SELECTOR,
                                                 f"#accrualsHistoryTable tbody td:nth-child({number_column})")
            list_sort_actual = [el.text for el in actual_result]
            list_sort_actual = [item.replace(" ", "") for item in list_sort_actual]

            assert list_sort_exp == list_sort_actual

        except TimeoutException:
            assert check_exists_by_xpath(".col-12.widget-accruals", driver)

    # История начислений: Проверка значений ИТОГО (Входящее сальдо)
    def test_total_in(self, config, driver, login_lk):
        driver.get(f"{config['link']}/{config['account']['base_code']}/account/{config['account']['ls']}/accruals")
        try:
            WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR,
                                                                                   ".col-12.widget-accruals")))
            history = driver.find_element(By.CSS_SELECTOR, "#archive-tab")
            history.click()

            sum_in = driver.find_element(By.CSS_SELECTOR,
                                         "#accrualsHistoryTable tbody tr:nth-child(1) td:nth-child(2)").text.replace(" ", "")

            in_balance = driver.find_element(By.CSS_SELECTOR, "#accrualsHistoryTable thead th:nth-child(2)")
            in_balance.click()

            sum_total_in = driver.find_element(By.CSS_SELECTOR, "#accrualsHistoryTable tfoot th:nth-child(2)").text
            sum_total_in = sum_total_in.replace(" ", "")
            assert sum_in == sum_total_in, allure.attach(f"expected: {sum_in}"
                                                         f"\nactual: {sum_total_in}")

        except TimeoutException:
            assert check_exists_by_xpath(".col-12.widget-accruals", driver)

    # История начислений: Проверка значений ИТОГО
    @pytest.mark.parametrize("number_column", ["3", "4", "5", "6", "7"])
    def test_total_accrued(self, config, driver, login_lk, number_column):
        driver.get(f"{config['link']}/{config['account']['base_code']}/account/{config['account']['ls']}/accruals")
        try:
            WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR,
                                                                                   ".col-12.widget-accruals")))
            history = driver.find_element(By.CSS_SELECTOR, "#archive-tab")
            history.click()

            time.sleep(1)

            sum_accrued = driver.find_elements(By.CSS_SELECTOR,
                                               f"#accrualsHistoryTable tbody tr td:nth-child({number_column})")

            sum_list_float = [item.text for item in sum_accrued]
            list_exp = [float(item.replace(" ", "")) for item in sum_list_float]
            sum_float = sum(list_exp)
            sum_float = round(sum_float, 2)

            sort_column = driver.find_element(By.CSS_SELECTOR, f"#accrualsHistoryTable thead th:nth-child({number_column})")
            sort_column.click()
            time.sleep(1)

            sum_total = driver.find_element(By.CSS_SELECTOR, f"#accrualsHistoryTable tfoot th:nth-child({number_column})").text
            sum_total = sum_total.replace(" ", "")

            assert float(sum_total) == sum_float, allure.attach(f"expected: {str(sum_float)}"
                                                                   f"\nactual: {sum_total}")

        except TimeoutException:
            assert check_exists_by_xpath(".col-12.widget-accruals", driver)

    # История платежей: вывод данных за указанный период
    def test_payment_history(self,  config, driver, login_lk):
        driver.get(f"{config['link']}/{config['account']['base_code']}/account/{config['account']['ls']}/accruals")
        try:
            WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR,
                                                                                   ".col-12.widget-accruals")))
            history = driver.find_element(By.CSS_SELECTOR, "#payments-tab")
            history.click()

            list_exp = []
            from_d = "03.12.2020"
            to_d = "31.01.2021"
            date_from = datetime.strptime(from_d, "%d.%m.%Y")
            date_to = datetime.strptime(to_d, "%d.%m.%Y")

            list_dates = driver.find_elements(By.CSS_SELECTOR, "#paymentsHistoryTable td span")

            for el in list_dates:
                date_format = datetime.strptime(el.text, "%d.%m.%y")
                if (date_format > date_from) & (date_format < date_to):
                    list_exp.append(el.text)

            input_date_from = driver.find_element(By.CSS_SELECTOR, "#paymentsHistoryFrom")
            input_date_from.send_keys(Keys.BACKSPACE*10)
            input_date_from.send_keys(from_d)
            driver.find_element(By.CSS_SELECTOR, ".active.day").click()

            input_date_to = driver.find_element(By.CSS_SELECTOR, "#paymentsHistoryTo")
            input_date_to.send_keys(Keys.BACKSPACE * 10)
            input_date_to.send_keys(to_d)
            driver.find_element(By.CSS_SELECTOR, ".active.day").click()
                   
            time.sleep(1)

            list_dates_actual = driver.find_elements(By.CSS_SELECTOR, "#paymentsHistoryTable td span")
            list_dates_actual = [el.text for el in list_dates_actual]

            assert list_exp == list_dates_actual

        except TimeoutException:
            assert check_exists_by_xpath(".col-12.widget-accruals", driver)
