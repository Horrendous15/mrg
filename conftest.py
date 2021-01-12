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

@pytest.fixture(scope='session')
def config():
    with open('config.json') as config_file:
        data = json.load(config_file)
    return data

@pytest.fixture(scope='session')
@pytest.fixture
def driver(config):
    if config['browser'] == 'chrome':
        driver = webdriver.Chrome()
    elif config['browser'] == 'firefox':
        driver = webdriver.Firefox()
    else:
        raise Exception(f'{config["browser"]} is not a supported browser')
    login_lk(driver, config)
    yield driver
    driver.quit()


def login_lk(driver, config):
    driver.get("link")
    # driver.set_window_size(1500, 1200)
    driver.implicitly_wait(10)

    driver.find_element(By.ID)