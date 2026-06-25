import os
import pytest
import my_practice_form_po


@pytest.fixture
def tmp_file():
    file_path = os.path.abspath("test_file.jpg")
    with open(file_path, "w") as file:
        file.write("Test")
    yield file_path
    if os.path.exists(file_path):
        os.remove(file_path)


URL = "https://qa-guru.github.io/one-page-form/automation-practice-form.html"


def test_form_positive01(driver, tmp_file):
    page = my_practice_form_po.PracticeFormPO(driver)
    driver.get(URL)
    page.fill_in_form(
        tmp_file,
        "Anna",
        "Cica",
        "anna@example.com",
        "Female",
        "0987654321",
        ("2000", "5", "22"),
        ("Maths", "English"),
        ("Reading", "Music"),
        "г. Красноярск, ул. Ленинский проспект, д 10",
        "NCR",
        "Noida",
    )
    page.assert_form(
        tmp_file,
        "Anna",
        "Cica",
        "anna@example.com",
        "Female",
        "0987654321",
        ("2000", "5", "22"),
        ("Maths", "English"),
        ("Reading", "Music"),
        "г. Красноярск, ул. Ленинский проспект, д 10",
        "NCR",
        "Noida",
    )


def test_form_positive02(driver, tmp_file):
    page = my_practice_form_po.PracticeFormPO(driver)
    driver.get(URL)
    page.fill_in_form(
        tmp_file,
        "Dmitry",
        "Bugaev",
        "bugaev@example.com",
        "Male",
        "1234567890",
        ("1988", "4", "22"),
        ("Maths", "English"),
        ("Sports", "Music"),
        "г. Санкт-Петербург, ул. Невский проспект, д 101",
        "Haryana",
        "Panipat",
    )
    page.assert_form(
        tmp_file,
        "Dmitry",
        "Bugaev",
        "bugaev@example.com",
        "Male",
        "1234567890",
        ("1988", "4", "22"),
        ("Maths", "English"),
        ("Sports", "Music"),
        "г. Санкт-Петербург, ул. Невский проспект, д 101",
        "Haryana",
        "Panipat",
    )
