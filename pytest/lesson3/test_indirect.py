import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

SIGN_UP_LOCATOR = (By.CSS_SELECTOR, "a.HeaderMenu-link--sign-up[href^='/signup']")
MOBILE_MENU_TOGGLE = (
    By.CSS_SELECTOR,
    "button.js-header-menu-toggle[aria-label='Toggle navigation']",
)

DESKTOP_SIZES = [(1920, 1080), (1440, 900)]
MOBILE_SIZES = [(375, 812), (414, 896)]


@pytest.mark.parametrize("browser_size", DESKTOP_SIZES, indirect=True)
def test_desktop_sign_up_indirect(browser_size):
    browser_size.find_element(*SIGN_UP_LOCATOR).click()
    assert "/signup" in browser_size.current_url


@pytest.mark.parametrize("browser_size", MOBILE_SIZES, indirect=True)
def test_mobile_sign_up_indirect(browser_size):
    menu_button = WebDriverWait(browser_size, 10).until(
        EC.element_to_be_clickable(MOBILE_MENU_TOGGLE)
    )
    menu_button.click()

    sign_up_link = WebDriverWait(browser_size, 10).until(
        EC.element_to_be_clickable(SIGN_UP_LOCATOR)
    )
    sign_up_link.click()
    assert "/signup" in browser_size.current_url
