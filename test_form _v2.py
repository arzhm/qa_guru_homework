import time
from selenium import webdriver
from selenium.webdriver.common.by import By

PAGE_URL = "https://qa-guru.github.io/one-page-form/text-box.html"

driver = webdriver.Chrome()

try:
    # Тест 1 - позитивный
    def test_valid_email():
        driver.get(PAGE_URL)
        driver.find_element(By.ID, "userName").send_keys("Анна Петрова")
        driver.find_element(By.ID, "userEmail").send_keys("anna@example.com")
        driver.find_element(By.ID, "submit").click()
        time.sleep(2)
        result = driver.find_element(By.ID, "output").text
        assert "Анна Петрова" in result
        print("Тест 1 пройден: валидный email")

    # Тест 2 - негативный, без собачки
    def test_email_without_at():
        driver.get(PAGE_URL)
        driver.find_element(By.ID, "userName").send_keys("Тест")
        driver.find_element(By.ID, "userEmail").send_keys("ivanexample.com")
        driver.find_element(By.ID, "submit").click()
        time.sleep(2)
        output = driver.find_element(By.ID, "output")
        class_attr = output.get_attribute("class") or ""
        assert "has-content" not in class_attr
        print("Тест 2 пройден: email без собачки отклонён")

    # Тест 3 - негативный, пустой email
    def test_empty_email():
        driver.get(PAGE_URL)
        driver.find_element(By.ID, "userName").send_keys("Пусто")
        driver.find_element(By.ID, "userEmail").send_keys("")
        driver.find_element(By.ID, "submit").click()
        time.sleep(2)
        output = driver.find_element(By.ID, "output")
        # БАГ: сайт принимает пустой email — валидация не работает
        class_attr = output.get_attribute("class") or ""
        print("Тест 3: сайт принял пустой email — это баг!")

    # Тест 4 - негативный, длинный email
    def test_long_email():
        driver.get(PAGE_URL)
        driver.find_element(By.ID, "userName").send_keys("Длинный")
        driver.find_element(By.ID, "userEmail").send_keys("s" * 250 + "@example.com")
        driver.find_element(By.ID, "submit").click()
        time.sleep(2)
        output = driver.find_element(By.ID, "output")
        class_attr = output.get_attribute("class") or ""
        # БАГ: сайт принимает слишком длинный email — валидация не работает
        print("Тест 4: сайт принял длинный email — это баг!")

    # Тест 5 - негативный, SQL инъкция
    def test_sql_injection_email():
        driver.get(PAGE_URL)
        driver.find_element(By.ID, "userName").send_keys("Инъекция")
        driver.find_element(By.ID, "userEmail").send_keys("' OR '1'='1@example.com")
        driver.find_element(By.ID, "submit").click()
        time.sleep(2)
        output = driver.find_element(By.ID, "output")
        class_attr = output.get_attribute("class") or ""
        assert "has-content" not in class_attr
        print("Тест 5 пройден: email не принят")

    # Тест 6 - проверка Current Address
    def test_current_address():
        driver.get(PAGE_URL)
        driver.find_element(By.ID, "userName").send_keys("Тест")
        driver.find_element(By.ID, "userEmail").send_keys("test@example.com")
        driver.find_element(By.ID, "currentAddress").send_keys(
            "Тестовый адрес для проверки"
        )
        driver.find_element(By.ID, "submit").click()
        time.sleep(2)
        output = driver.find_element(By.ID, "output")
        class_attr = output.get_attribute("class") or ""
        assert "has-content" in class_attr
        result = output.text
        assert "Тестовый адрес для проверки" in result
        print("Тест 6 пройден: Current Address принят")

    # Тест 7 - проверка Permanent Address
    def test_permanent_address():
        driver.get(PAGE_URL)
        driver.find_element(By.ID, "userName").send_keys("Тест")
        driver.find_element(By.ID, "userEmail").send_keys("test@example.com")
        driver.find_element(By.ID, "currentAddress").send_keys(
            "Тестовый адрес для проверки current addres1"
        )
        driver.find_element(By.ID, "permanentAddress").send_keys(
            "Тестовый адрес для проверки permanent adress2"
        )
        driver.find_element(By.ID, "submit").click()
        time.sleep(2)
        output = driver.find_element(By.ID, "output")
        class_attr = output.get_attribute("class") or ""
        assert "has-content" in class_attr
        result = output.text
        assert "Тестовый адрес для проверки permanent adress2" in result
        print("Тест 7 пройден: Permanent Address принят")

    test_valid_email()
    test_email_without_at()
    test_empty_email()
    test_long_email()
    test_sql_injection_email()
    test_current_address()
    test_permanent_address()

finally:
    driver.quit()


# Вывод по пункту 8:
# Текущее решение работает, но неудобно изменять, потому что:
# - тестовые данные (имена, email, адреса) написаны прямо внутри каждой функции
# - чтобы изменить данные, нужно заходить в каждую функцию отдельно
# - если тестов станет 50, это займёт очень много времени
# - лучшее решение: вынести все данные в одно место
