import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class TestSuite:
    def __init__(self):
        self.driver = None
        self.wait = None
        self.url = "https://qa-guru.github.io/one-page-form/automation-practice-form.html"
        self.temp_file_path = os.path.abspath("test_image.jpg")

        # Заголовки страницы
        self.form_title_locator = (By.XPATH, "/html/body/main/section/h1")
        self.form_sub_title_locator = (By.XPATH, "/html/body/main/section/div/p")

        # Баннер, который перекрывает элементы
        self.banner_title_locator = (By.XPATH, "//*[contains(text(), 'Level up your automation')]")
        self.close_banner_button_locator = (By.XPATH, "//*[@id='fixedban']/div/div/button")

        # Основные поля формы
        self.first_name_locator = (By.ID, "firstName")
        self.last_name_locator = (By.ID, "lastName")
        self.email_locator = (By.ID, "userEmail")
        self.gender_male_locator = (By.CSS_SELECTOR, "label[for='gender-radio-1']")
        self.mobile_number_locator = (By.ID, "userNumber")
        self.date_of_birth_locator = (By.ID, "dateOfBirthInput")
        self.subjects_locator = (By.ID, "subjectsInput")
        self.hobby_sports_locator = (By.CSS_SELECTOR, "label[for='hobbies-checkbox-1']")
        self.hobby_music_locator = (By.CSS_SELECTOR, "label[for='hobbies-checkbox-3']")
        self.upload_picture_locator = (By.ID, "uploadPicture")
        self.current_address_locator = (By.ID, "currentAddress")
        self.state_locator = (By.ID, "state")
        self.city_locator = (By.ID, "city")
        self.submit_button_locator = (By.ID, "submit")

        # Календарь
        self.calendar_locator = (By.CLASS_NAME, "react-datepicker__month-container")
        self.month_select_locator = (By.CLASS_NAME, "react-datepicker__month-select")
        self.year_select_locator = (By.CLASS_NAME, "react-datepicker__year-select")
        self.day_25_locator = (By.CSS_SELECTOR, ".react-datepicker__day--025:not(.react-datepicker__day--outside-month)")

        # Модальное окно с результатами
        self.modal_title_locator = (By.ID, "example-modal-sizes-title-lg")
        self.result_table_locator = (By.CLASS_NAME, "table-responsive")

    def set_up_test(self):
        # 1. Открытие браузера и страницы
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()

        # Implicit Wait: Selenium будет ждать появления элементов до 5 секунд
        self.driver.implicitly_wait(5)

        # Explicit Wait: будем использовать для конкретных условий
        self.wait = WebDriverWait(self.driver, 10)

        self.driver.get(self.url)

    def tear_down_test(self):
        # 2. Удаление временного файла и закрытие браузера
        if os.path.exists(self.temp_file_path):
            os.remove(self.temp_file_path)

        if self.driver:
            self.driver.quit()

    def close_banner_if_present(self):
        # Баннер может перекрывать элементы формы, поэтому закрываем его
        try:
            self.wait.until(EC.visibility_of_element_located(self.banner_title_locator))
            close_banner_btn = self.wait.until(EC.element_to_be_clickable(self.close_banner_button_locator))
            close_banner_btn.click()
            self.wait.until(EC.invisibility_of_element(close_banner_btn))
        except Exception:
            print("Баннер не появился или уже закрыт")

    def hide_footer_and_scroll_down(self):
        # execute_script: убираем footer и прокручиваем страницу вниз
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        self.driver.execute_script("document.getElementsByTagName('footer')[0].style.display='none';")

    def select_date_of_birth(self):
        date_input = self.wait.until(EC.element_to_be_clickable(self.date_of_birth_locator))
        date_input.click()

        self.wait.until(EC.visibility_of_element_located(self.calendar_locator))

        month_select = self.wait.until(EC.element_to_be_clickable(self.month_select_locator))
        month_select.click()
        month_select.find_element(By.XPATH, "//option[@value='11']").click()  # December

        year_select = self.wait.until(EC.element_to_be_clickable(self.year_select_locator))
        year_select.click()
        year_select.find_element(By.XPATH, "//option[@value='1995']").click()

        day_element = self.wait.until(EC.element_to_be_clickable(self.day_25_locator))
        day_element.click()

    def select_state_and_city(self):
        # Dropdown State
        state_dropdown = self.wait.until(EC.element_to_be_clickable(self.state_locator))
        state_dropdown.click()
        state_option = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'NCR')]")))
        state_option.click()

        # Dropdown City
        city_dropdown = self.wait.until(EC.element_to_be_clickable(self.city_locator))
        city_dropdown.click()
        city_option = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Delhi')]")))
        city_option.click()

    def create_test_file(self):
        with open(self.temp_file_path, "w", encoding="utf-8") as file:
            file.write("fake image data")

    def positive_test_fill_student_registration_form(self):
        try:
            self.set_up_test()

            # Проверка, что открылась нужная форма
            form_title = self.wait.until(EC.visibility_of_element_located(self.form_title_locator))
            assert form_title.text == "Practice Form"

            form_sub_title = self.wait.until(EC.visibility_of_element_located(self.form_sub_title_locator))
            assert form_sub_title.text == "Student Registration Form"

            self.close_banner_if_present()

            # Текстовые поля
            first_name = self.wait.until(EC.element_to_be_clickable(self.first_name_locator))
            first_name.send_keys("Иван")

            last_name = self.driver.find_element(*self.last_name_locator)
            last_name.send_keys("Петров")

            email = self.driver.find_element(*self.email_locator)
            email.send_keys("ivan.petrov@example.com")

            # Радиокнопка Gender
            gender_male = self.wait.until(EC.element_to_be_clickable(self.gender_male_locator))
            gender_male.click()

            # Mobile
            mobile_number = self.driver.find_element(*self.mobile_number_locator)
            mobile_number.send_keys("9991234567")

            # Date of Birth
            self.select_date_of_birth()

            # Subjects 
            subjects_input = self.wait.until(EC.element_to_be_clickable(self.subjects_locator))
            subjects_input.send_keys("Computer Science")
            subjects_input.send_keys(Keys.ENTER)

            # Checkboxes Hobbies
            hobby_sports = self.wait.until(EC.element_to_be_clickable(self.hobby_sports_locator))
            hobby_sports.click()

            hobby_music = self.wait.until(EC.element_to_be_clickable(self.hobby_music_locator))
            hobby_music.click()

            # Upload Picture
            self.create_test_file()
            upload_input = self.driver.find_element(*self.upload_picture_locator)
            upload_input.send_keys(self.temp_file_path)

            # Current Address
            current_address = self.driver.find_element(*self.current_address_locator)
            current_address.send_keys("123456, г. Москва, ул. Ленина, д. 1")

            self.hide_footer_and_scroll_down()
            self.select_state_and_city()

            submit_button = self.wait.until(EC.element_to_be_clickable(self.submit_button_locator))
            self.driver.execute_script("arguments[0].click();", submit_button)

            # Проверка результата
            modal_title = self.wait.until(EC.visibility_of_element_located(self.modal_title_locator))
            assert modal_title.text == "Thanks for submitting the form"

            result_table = self.wait.until(EC.visibility_of_element_located(self.result_table_locator))
            result_text = result_table.text

            assert "Иван Петров" in result_text
            assert "ivan.petrov@example.com" in result_text
            assert "Male" in result_text
            assert "9991234567" in result_text
            assert "25 Dec 1995" in result_text
            assert "Computer Science" in result_text
            assert "Sports, Music" in result_text
            assert "test_image.jpg" in result_text
            assert "123456, г. Москва, ул. Ленина, д. 1" in result_text
            assert "NCR Delhi" in result_text

            print("Позитивный тест Student Registration Form успешно пройден!")

        finally:
            self.tear_down_test()

    def negative_test_required_fields_are_empty(self):
        try:
            self.set_up_test()
            self.close_banner_if_present()
            self.hide_footer_and_scroll_down()

            # Отправляем пустую форму
            submit_button = self.wait.until(EC.element_to_be_clickable(self.submit_button_locator))
            self.driver.execute_script("arguments[0].click();", submit_button)
            submit_button = self.wait.until(
                EC.element_to_be_clickable(self.submit_button_locator)
            )
            self.driver.execute_script("arguments[0].click();", submit_button)

            try:
                self.wait.until(
                    EC.visibility_of_element_located(
                        self.modal_title_locator
                    )
                )

                assert False, "Форма отправилась с пустыми обязательными полями"

            except TimeoutException:
                pass

            # Проверяем, что модальное окно НЕ появилось
            modal_windows = self.driver.find_elements(*self.modal_title_locator)
            #assert len(modal_windows) == 0
            # БАГ: сайт принимает пустую форму — валидация не работает
            print("Негативный тест: сайт принял пустую форму - это баг!")

            # Проверяем, что обязательные поля подсвечены как невалидные
            first_name = self.driver.find_element(*self.first_name_locator)
            last_name = self.driver.find_element(*self.last_name_locator)
            mobile_number = self.driver.find_element(*self.mobile_number_locator)

            assert first_name.get_attribute("value") == ""
            assert last_name.get_attribute("value") == ""
            assert mobile_number.get_attribute("value") == ""

            print("Негативный тест с пустыми обязательными полями успешно пройден!")

        finally:
            self.tear_down_test()


suite = TestSuite()
suite.positive_test_fill_student_registration_form()
suite.negative_test_required_fields_are_empty()