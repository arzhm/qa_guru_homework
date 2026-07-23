from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

SIGN_UP_LOCATOR = (By.CSS_SELECTOR, "a.HeaderMenu-link--sign-up[href^='/signup']")
MOBILE_MENU_TOGGLE = (By.CSS_SELECTOR, "button.js-header-menu-toggle[aria-label='Toggle navigation']")


def test_desktop_sign_up_fixture(desktop_browser):
    desktop_browser.find_element(*SIGN_UP_LOCATOR).click()
    assert "/signup" in desktop_browser.current_url


def test_mobile_sign_up_fixture(mobile_browser):
    menu_button = WebDriverWait(mobile_browser, 10).until(
        EC.element_to_be_clickable(MOBILE_MENU_TOGGLE)
    )
    menu_button.click()

    sign_up_link = WebDriverWait(mobile_browser, 10).until(
        EC.element_to_be_clickable(SIGN_UP_LOCATOR)
    )
    sign_up_link.click()
    assert "/signup" in mobile_browser.current_url