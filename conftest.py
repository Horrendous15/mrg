import pytest
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By


@pytest.fixture(scope='session')
def config():
    with open('config.json', encoding="utf-8") as config_file:
        data = json.load(config_file)
    return data


@pytest.fixture
def driver(config):
    if config['browser'] == 'chrome':
        driver = webdriver.Chrome()
    elif config['browser'] == 'firefox':
        driver = webdriver.Firefox()
    elif config['browser'] == 'edge':
        driver = webdriver.Edge("C:\\Webdriver\\msedgedriver.exe")
    else:
        raise Exception(f'{config["browser"]} is not a supported browser')
    # login_lk(driver, config)
    yield driver
    driver.quit()


@pytest.fixture
def login_lk(driver, config):
    try:
        driver.get(f"{config['link']}")
        # driver.set_window_size(1500, 1200)
        driver.implicitly_wait(10)

        logininput = driver.find_element(By.CSS_SELECTOR, "#authorization_form .form-group:nth-child(2) .form-control")
        logininput.send_keys(f"{config['login_auth']}")

        passinput = driver.find_element(By.CSS_SELECTOR, "#authorization_form .form-group:nth-child(3) .form-control")
        passinput.send_keys(f"{config['pass_auth']}")

        button = driver.find_element(By.CSS_SELECTOR, "#authorization_form .btn")
        button.click()

    except Exception:
        print("\nошибка аторизации")
        driver.close()