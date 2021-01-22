import pytest
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By


@pytest.fixture(scope='session')
def config():
    with open('tests/config.json', encoding="utf-8") as config_file:
        data = json.load(config_file)
    return data


@pytest.fixture
def driver(config):
    if config['browser'] == 'chrome':
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        driver = webdriver.Chrome(options=options)
    elif config['browser'] == 'firefox':

        fp = webdriver.FirefoxProfile()
        fp.set_preference("browser.download.folderList", 2)
        fp.set_preference("browser.download.manager.showWhenStarting", False)
        fp.set_preference("browser.helperApps.alwaysAsk.force", False)
        fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf")
        fp.set_preference("pdfjs.disabled", True)
        driver = webdriver.Firefox(fp)
    elif config['browser'] == 'edge':
        driver = webdriver.Edge("C:\\Webdriver\\msedgedriver.exe")
    else:
        raise Exception(f'{config["browser"]} is not a supported browser')
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
