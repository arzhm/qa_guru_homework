import pytest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# URL тестируемой страницы
URL = "https://qa-guru.github.io/one-page-form/login.html"

# Локаторы элементов формы на странице
LOGIN_INPUT = (By.ID, "login-input")
PASSWORD_INPUT = (By.ID, "password-input")
SUBMIT_BUTTON = (By.ID, "submit-button")
ERROR_MESSAGE = (By.ID, "error-message")
WELCOME_MESSAGE = (By.ID, "welcome-message")


@pytest.fixture
def driver():
    """Фикстура для инициализации и закрытия браузера."""
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(5)

    yield driver

    driver.quit()


# Реализация DDT подхода через параметризацию pytest
@pytest.mark.parametrize(
    "login, password, scenario_type, expected_text",
    [
        # --- ПОЗИТИВНЫЙ СЦЕНАРИЙ ---
        ("user1", "password1", "positive", "Welcome"),

        # --- НЕГАТИВНЫЕ СЦЕНАРИИ ---
        ("negativ@test.ru", "123456", "negative", "Wrong login or password"),
        ("", "123456", "negative", "Login is required (minimum 3 characters)"),
        ("test@test.ru", "", "negative", "Password is required (minimum 6 characters)"),

        # --- ДОПОЛНИТЕЛЬНЫЕ НЕГАТИВНЫЕ СЦЕНАРИИ ---
        ("ab", "123456", "negative", "Login must be at least 3 characters"),
        ("test@test.ru", "12345", "negative", "Password must be at least 6 characters"),
        ("", "", "negative", "Login and password are required (minimum 3 and 6 characters)"),
        ("' OR '1'='1", "' OR '1'='1", "negative", "Wrong login or password"),
    ]
)
def test_login_form(driver, login, password, scenario_type, expected_text):
    """Тест-кейс, принимающий наборы данных (DDT)."""

    # 1. Открытие тестируемой страницы
    driver.get(URL)

    # 2. Поиск элементов формы
    login_field = driver.find_element(*LOGIN_INPUT)
    password_field = driver.find_element(*PASSWORD_INPUT)
    submit_button = driver.find_element(*SUBMIT_BUTTON)

    # 3. Очистка полей и ввод тестовых данных
    login_field.clear()
    login_field.send_keys(login)

    password_field.clear()
    password_field.send_keys(password)

    # 4. Клик по кнопке отправки формы
    submit_button.click()

    # 5. Проверка результата
    if scenario_type == "positive":
        welcome_message = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located(WELCOME_MESSAGE)
        )

        assert expected_text in welcome_message.text, \
            f"Ожидался успешный вход, но получено: '{welcome_message.text}'"
        assert login in welcome_message.text, \
            f"В приветствии должен быть логин '{login}', но получено: '{welcome_message.text}'"

    else:
        error_message = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located(ERROR_MESSAGE)
        )

        assert expected_text in error_message.text, \
            f"Ожидалась ошибка '{expected_text}', но получено: '{error_message.text}'"