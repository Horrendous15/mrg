import pytest
import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By


@pytest.fixture(scope='session')
def config():
    with open('config.json', encoding="utf-8") as config_file:
        data = json.load(config_file)
    return data


@pytest.fixture
def driver(config):
    if config["browser"] == 'chrome':
        options = webdriver.ChromeOptions()
        options.add_experimental_option("prefs", {
            'download.default_directory': config["path_to_download"],
            'download.prompt_for_download': False,
            'download.directory_upgrade': True,
  })
        options.add_argument('headless')
        driver = webdriver.Chrome(options=options)

        # driver = webdriver.Chrome()
    else:
        raise Exception(f'{config["browser"]} is not a supported browser')
    yield driver
    driver.quit()


@pytest.fixture
def login_lk(driver, config):
    try:
        driver.get(f"{config['link']}")
        driver.set_window_size(1500, 1200)
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