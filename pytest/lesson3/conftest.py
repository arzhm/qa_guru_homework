import pytest
from selenium import webdriver

DESKTOP_SIZES = [(1920, 1080), (1440, 900)]
MOBILE_SIZES = [(375, 812), (414, 896)]
ALL_SIZES = DESKTOP_SIZES + MOBILE_SIZES

BREAKPOINT_WIDTH = 1012  # ниже этой ширины github прячет Sign up в гамбургер-меню


def _make_driver(width, height):
    driver = webdriver.Chrome()
    driver.set_window_size(width, height)
    driver.get("https://github.com/")
    return driver


# ---------- Подход 1: skip по условию ----------
@pytest.fixture(params=ALL_SIZES)
def setup_browser(request):
    width, height = request.param
    driver = _make_driver(width, height)
    device_type = "desktop" if width >= BREAKPOINT_WIDTH else "mobile"
    yield driver, device_type
    driver.quit()


# ---------- Подход 2: indirect ----------
@pytest.fixture
def browser_size(request):
    width, height = request.param
    driver = _make_driver(width, height)
    yield driver
    driver.quit()


# ---------- Подход 3: разные фикстуры под каждый тест ----------
@pytest.fixture(params=DESKTOP_SIZES)
def desktop_browser(request):
    width, height = request.param
    driver = _make_driver(width, height)
    yield driver
    driver.quit()


@pytest.fixture(params=MOBILE_SIZES)
def mobile_browser(request):
    width, height = request.param
    driver = _make_driver(width, height)
    yield driver
    driver.quit()