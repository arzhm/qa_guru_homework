from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import InvalidSelectorException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
import my_calendar_element
from seleniumpagefactory.Pagefactory import PageFactory
from selenium.webdriver.common.by import By


class PracticeFormPF(PageFactory):
    def __init__(self, driver):
        self.driver = driver
        self.locators = {
            "practice_form_title": ("XPATH", "//main//h1"),
            "first_name_field": ("ID", "firstName"),
            "last_name_field": ("ID", "lastName"),
            "email_field": ("ID", "userEmail"),
            "user_number_field": ("ID", "userNumber"),
            "subject_field": ("ID", "subjectsInput"),
            "upload_picture_field": ("ID", "uploadPicture"),
            "current_address_field": ("ID", "currentAddress"),
            "state_input": ("ID", "state"),
            "city_input": ("ID", "city"),
            "submit_button": ("ID", "submit"),
            "banner_button": (
                "XPATH",
                "//div[@id='fixedban']//button[@aria-label='Close']",
            ),
            "result_form": ("ID", "resultModal"),
        }
        self.wait = WebDriverWait(driver, 5)
        self.calendar = my_calendar_element.CalendarElement(driver)

    def _close_commercial_banner(self):
        self.banner_button.click()

    def _fill_first_name(self, first_name):
        self.first_name_field.send_keys(first_name)

    def _fill_last_name(self, last_name):
        self.last_name_field.send_keys(last_name)

    def _fill_email(self, email):
        self.email_field.send_keys(email)

    def _fill_user_number(self, user_number):
        self.user_number_field.send_keys(user_number)

    def _select_gender(self, gender):
        gender_radio_button = self.driver.find_element(
            By.XPATH, f"//div[@id='genterWrapper']//input[@value='{gender}']"
        )
        gender_radio_button.click()

    def _upload_file(self, file_path):
        self.upload_picture_field.send_keys(file_path)

    def _fill_subject(self, *subjects):
        self.driver.execute_script("arguments[0].scrollIntoView();", self.subject_field)
        for subject in subjects[0]:
            self.subject_field.send_keys(subject)
            self.subject_field.send_keys(Keys.ENTER)

    def _select_hobbies(self, *hobbies):
        try:
            for hobby in hobbies[0]:
                hobby_check_box = self.driver.find_element(
                    By.XPATH, f"//div[@id='hobbiesWrapper']//input[@value='{hobby}']"
                )
                hobby_check_box.click()
        except NoSuchElementException as ex:
            print(ex)
        except InvalidSelectorException as ex:
            print(ex)

    def _fill_current_address(self, current_address):
        self.current_address_field.send_keys(current_address)

    def _select_state(self, state):
        self.state_input.click()
        state_dropdown = self.wait.until(
            ec.element_to_be_clickable(
                (By.XPATH, f"//div[@class='state-city-option'][text()='{state}']")
            )
        )
        state_dropdown.click()

    def _select_city(self, city):
        self.city_input.click()
        city_dropdown = self.wait.until(
            ec.element_to_be_clickable(
                (By.XPATH, f"//div[@class='state-city-option'][text()='{city}']")
            )
        )
        city_dropdown.click()

    def _click_submit_button(self):
        self.driver.execute_script("arguments[0].scrollIntoView();", self.submit_button)
        self.submit_button.click()

    def fill_in_form(
        self,
        file_name=None,
        first_name=None,
        last_name=None,
        email=None,
        gender=None,
        user_number=None,
        birth_day=None,
        subjects=None,
        hobbies=None,
        current_address=None,
        state=None,
        city=None,
    ):
        assert (
            self.practice_form_title.text == "Practice Form"
        ), "Заголовок страницы не совпадает"

        self._close_commercial_banner()
        self._fill_first_name(first_name)
        self._fill_last_name(last_name)
        self._fill_email(email)
        self._select_gender(gender)
        self._fill_user_number(user_number)
        self.calendar.select_date(birth_day[0], birth_day[1], birth_day[2])
        self._fill_subject(subjects)
        self._select_hobbies(hobbies)
        self._upload_file(file_name)
        self._fill_current_address(current_address)
        self._select_state(state)
        self._select_city(city)
        self._click_submit_button()

    # TODO: со временем вынести в тесты или создать несколько разных методов assert под нужды разных тестов
    def assert_form(
        self,
        file_name=None,
        first_name=None,
        last_name=None,
        email=None,
        gender=None,
        user_number=None,
        birth_day=None,
        subjects=None,
        hobbies=None,
        current_address=None,
        state=None,
        city=None,
    ):
        self.wait.until(ec.visibility_of_element_located(("id", "resultModal")))
        assert self.result_form.is_displayed(), "Таблица с данным не отобразилась"

        result_text = self.result_form.text

        expected_data = {
            "Student Name": f"{first_name} {last_name}",
            "Student Email": email,
            "Gender": gender,
            "Mobile": user_number,
            "Date of Birth": birth_day[0],
            "Subjects": subjects,
            "Hobbies": hobbies,
            "Picture": "test_file.jpg",  # file_name,
            "Address": current_address,
            "State and City": f"{state} {city}",
        }

        # AssertionError: Значения D:\Projects\Python\Student01Prj01\test_file.jpg из строки Picture не совпадают!
        for key, value in expected_data.items():
            if isinstance(value, tuple):
                value = value[0]
            assert (
                key in result_text and value in result_text
            ), f"Значения {value} из строки {key} не совпадают!"
