########################################################################################################################
# IMPORTS

import logging

import undetected_chromedriver as uc
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from .main import run_bash_command

########################################################################################################################
# FUNCTIONS

logger = logging.getLogger(__name__)


def get_chromedriver_version():
    return int(
        run_bash_command("/usr/bin/google-chrome --version")
        .split(" ")[2]
        .split(".")[0]
    )


def get_driver(chrome_options=None):
    options = uc.ChromeOptions()

    if isinstance(chrome_options, list):
        for option in chrome_options:
            options.add_argument(option)

    return uc.Chrome(version_main=get_chromedriver_version(),
                     options=options)


def wait(driver, css_selector, timeout=30):
    logger.info(f"waiting for {css_selector}...")
    return WebDriverWait(driver, timeout).until(EC.visibility_of_element_located(("css selector", css_selector)))


def wait_and_click(driver, css_selector, timeout=30):
    logger.info(f"clicking on {css_selector}...")
    wait(driver, css_selector, timeout).click()


def wait_and_fill(driver, css_selector, text_to_fill, timeout=30):
    logger.info(f"sending text to {css_selector}...")
    wait(driver, css_selector, timeout).send_keys(text_to_fill)


def scroll(driver, css_selector):
    element = wait(driver, css_selector)
    logger.info(f"scrolling to {css_selector}")
    driver.execute_script("arguments[0].scrollIntoView();",
                          element)


def scroll_and_click(driver, css_selector):
    element = wait(driver, css_selector)
    logger.info(f"scrolling to {css_selector}")
    driver.execute_script("arguments[0].scrollIntoView();",
                          element)

    logger.info(f"clicking to {css_selector}")
    element.click()


def press_key(driver, key):
    actions = ActionChains(driver)
    actions.send_keys(key).perform()
