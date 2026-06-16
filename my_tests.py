import time
from selenium import webdriver
from selenium.webdriver.common.by import By


def set_up_test(driver):
    # 1. Открытие страницы
    driver.get("https://qa-guru.github.io/one-page-form/login.html")
    driver.maximize_window()
    time.sleep(3)  # Пауза, чтобы визуально заметить открытие


def tear_down_test(driver):
    # 2. Закрытие браузера в любом случае
    driver.quit()


login_locator = (By.ID, "login-input")
password_locator = (By.ID, "password-input")
submit_button_locator = (By.ID, "submit-button")
error_message_locator = (By.ID, "error-message")


def positiv_test():
    driver = webdriver.Chrome()

    try:
        set_up_test(driver)

        # 3. Поиск элементов и заполнение полей

        login_field = driver.find_element(*login_locator)
        login_field.send_keys("test@test.ru")

        password_field = driver.find_element(*password_locator)
        password_field.send_keys("123456")

        submit_button = driver.find_element(*submit_button_locator)
        submit_button.click()

        time.sleep(3)

        print("Тест успешно пройден!")

    finally:
        tear_down_test(driver)


def negativ1_test():
    driver = webdriver.Chrome()

    try:
        set_up_test(driver)

        login_field = driver.find_element(*login_locator)
        login_field.send_keys("negativ@test.ru")

        password_field = driver.find_element(*password_locator)
        password_field.send_keys("123456")

        submit_button = driver.find_element(*submit_button_locator)
        submit_button.click()

        time.sleep(3)

        error_message = driver.find_element(*error_message_locator)

        assert "Wrong login or password" in error_message.text

        print("Тест успешно пройден!")

    finally:
        tear_down_test(driver)


def negativ2_test():
    driver = webdriver.Chrome()

    try:
        set_up_test(driver)

        login_field = driver.find_element(*login_locator)
        login_field.send_keys("")

        password_field = driver.find_element(*password_locator)
        password_field.send_keys("123456")

        submit_button = driver.find_element(*submit_button_locator)
        submit_button.click()
        time.sleep(3)
        error_message = driver.find_element(*error_message_locator)
        assert "Login is required (minimum 3 characters)" in error_message.text

        print("Тест успешно пройден!")
    finally:
        tear_down_test(driver)


def negativ3_test():
    driver = webdriver.Chrome()

    try:
        set_up_test(driver)

        login_field = driver.find_element(*login_locator)
        login_field.send_keys("test@test.ru")

        password_field = driver.find_element(*password_locator)
        password_field.send_keys("")

        submit_button = driver.find_element(*submit_button_locator)
        submit_button.click()
        time.sleep(3)
        error_message = driver.find_element(*error_message_locator)
        assert "Password is required (minimum 6 characters)" in error_message.text

        print("Тест успешно пройден!")

    finally:
        tear_down_test(driver)


positiv_test()
negativ1_test()
negativ2_test()
negativ3_test()
