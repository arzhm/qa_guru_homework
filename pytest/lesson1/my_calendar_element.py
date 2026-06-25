from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select


class CalendarElement:
    CALENDAR_INPUT = (By.ID, "dateOfBirthInput")
    YEAR_SELECT = (By.CSS_SELECTOR, ".react-datepicker__year-select")
    MONTH_SELECT = (By.CSS_SELECTOR, ".react-datepicker__month-select")

    def __init__(self, driver):
        self.driver = driver

    def select_date(self, year, month, day):
        self.driver.find_element(*self.CALENDAR_INPUT).click()
        Select(self.driver.find_element(*self.YEAR_SELECT)).select_by_value(year)
        Select(self.driver.find_element(*self.MONTH_SELECT)).select_by_value(month)
        self.driver.find_element(
            By.CSS_SELECTOR, f".react-datepicker__day--0{day}[tabindex='0']"
        ).click()
