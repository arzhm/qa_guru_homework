import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

SIGN_UP_LOCATOR = (By.CSS_SELECTOR, "a.HeaderMenu-link--sign-up[href^='/signup']")
MOBILE_MENU_TOGGLE = (
    By.CSS_SELECTOR,
    "button.js-header-menu-toggle[aria-label='Toggle navigation']",
)


def test_desktop_sign_up(setup_browser):
    driver, device_type = setup_browser
    if device_type == "mobile":
        pytest.skip("Узкое разрешение, десктопный тест не подходит")

    driver.find_element(*SIGN_UP_LOCATOR).click()
    assert "/signup" in driver.current_url


def test_mobile_sign_up(setup_browser):
    driver, device_type = setup_browser
    if device_type == "desktop":
        pytest.skip("Широкое разрешение, мобильный тест не подходит")

    menu_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(MOBILE_MENU_TOGGLE)
    )
    menu_button.click()

    sign_up_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(SIGN_UP_LOCATOR)
    )
    sign_up_link.click()
    assert "/signup" in driver.current_url
