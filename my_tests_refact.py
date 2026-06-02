import time
from selenium import webdriver
from selenium.webdriver.common.by import By


class TestSuite:
    def __init__(self):
        self.url = "https://qa-guru.github.io/one-page-form/login.html"
        self.login_locator = (By.ID, "login-input")
        self.password_locator = (By.ID, "password-input")
        self.submit_button_locator = (By.ID, "submit-button")
        self.error_message_locator = (By.ID, "error-message")

    def set_up_test(self):
        # 1. Открытие страницы
        self.driver.get(self.url)
        self.driver.maximize_window()
        time.sleep(3)  # Пауза, чтобы визуально заметить открытие

    def tear_down_test(self):
        # 2. Закрытие браузера в любом случае
        self.driver.quit()

    def positiv_test(self):

        try:
            self.driver = webdriver.Chrome()
            self.set_up_test()
            
            # 3. Поиск элементов и заполнение полей

            login_field = self.driver.find_element(*self.login_locator)
            login_field.send_keys("test@test.ru")

            password_field = self.driver.find_element(*self.password_locator)
            password_field.send_keys("123456")

            submit_button = self.driver.find_element(*self.submit_button_locator)
            submit_button.click()

            time.sleep(3)

            print("Тест успешно пройден!")

        finally:
            self.tear_down_test()

    def negativ1_test(self):

        try:
            self.driver = webdriver.Chrome()
            self.set_up_test()
           
            login_field = self.driver.find_element(*self.login_locator)
            login_field.send_keys("negativ@test.ru")

            password_field = self.driver.find_element(*self.password_locator)
            password_field.send_keys("123456")

            submit_button = self.driver.find_element(*self.submit_button_locator)
            submit_button.click()

            time.sleep(3)

            error_message = self.driver.find_element(*self.error_message_locator)

            assert "Wrong login or password" in error_message.text

            print("Тест успешно пройден!")

        finally:
            self.tear_down_test()

    def negativ2_test(self):

        try:
            self.driver = webdriver.Chrome()
            self.set_up_test()
            
            login_field = self.driver.find_element(*self.login_locator)
            login_field.send_keys("")

            password_field = self.driver.find_element(*self.password_locator)
            password_field.send_keys("123456")

            submit_button = self.driver.find_element(*self.submit_button_locator)
            submit_button.click()
            time.sleep(3)
            error_message = self.driver.find_element(*self.error_message_locator)
            assert "Login is required (minimum 3 characters)" in error_message.text

            print("Тест успешно пройден!")
        finally:
            self.tear_down_test()

    def negativ3_test(self):

        try:
            self.driver = webdriver.Chrome()
            self.set_up_test()

            login_field = self.driver.find_element(*self.login_locator)
            login_field.send_keys("test@test.ru")

            password_field = self.driver.find_element(*self.password_locator)
            password_field.send_keys("")

            submit_button = self.driver.find_element(*self.submit_button_locator)
            submit_button.click()
            time.sleep(3)
            error_message = self.driver.find_element(*self.error_message_locator)
            assert "Password is required (minimum 6 characters)" in error_message.text

            print("Тест успешно пройден!")

        finally:
            self.tear_down_test()


suite = TestSuite()
suite.positiv_test()
suite.negativ1_test()
suite.negativ2_test()
suite.negativ3_test()
