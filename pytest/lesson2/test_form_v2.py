import pytest
from selenium.webdriver.common.by import By

PAGE_URL = "https://qa-guru.github.io/one-page-form/text-box.html"


@pytest.mark.smoke
def test_valid_email(driver):
    driver.get(PAGE_URL)
    driver.find_element(By.ID, "userName").send_keys("Анна Петрова")
    driver.find_element(By.ID, "userEmail").send_keys("anna@example.com")
    driver.find_element(By.ID, "submit").click()
    result = driver.find_element(By.ID, "output").text
    assert "анна петрова" in result.strip().casefold()


@pytest.mark.integration
@pytest.mark.parametrize(
    "email",
    [
        "ivanexample.com",
        pytest.param(
            "", marks=pytest.mark.xfail(reason="баг: сайт принимает пустой email")
        ),
        pytest.param(
            "s" * 250 + "@example.com",
            marks=pytest.mark.xfail(reason="баг: сайт принимает длинный email"),
        ),
        "' OR '1'='1@example.com",
    ],
)
def test_invalid_email(driver, email):
    driver.get(PAGE_URL)
    driver.find_element(By.ID, "userName").send_keys("Тест")
    driver.find_element(By.ID, "userEmail").send_keys(email)
    driver.find_element(By.ID, "submit").click()
    output = driver.find_element(By.ID, "output")
    class_attr = output.get_attribute("class") or ""
    assert "has-content" not in class_attr


# Тест 6 - проверка Current Address
@pytest.mark.smoke
def test_current_address(driver):
    driver.get(PAGE_URL)
    driver.find_element(By.ID, "userName").send_keys("Тест")
    driver.find_element(By.ID, "userEmail").send_keys("test@example.com")
    driver.find_element(By.ID, "currentAddress").send_keys(
        "Тестовый адрес для проверки"
    )
    driver.find_element(By.ID, "submit").click()
    output = driver.find_element(By.ID, "output")
    class_attr = output.get_attribute("class") or ""
    assert "has-content" in class_attr
    result = output.text
    assert "Тестовый адрес для проверки" in result
    print("Тест 6 пройден: Current Address принят")


# Тест 7 - проверка Permanent Address
@pytest.mark.smoke
def test_permanent_address(driver):
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
    output = driver.find_element(By.ID, "output")
    class_attr = output.get_attribute("class") or ""
    assert "has-content" in class_attr
    result = output.text
    assert "Тестовый адрес для проверки permanent adress2" in result
    print("Тест 7 пройден: Permanent Address принят")
