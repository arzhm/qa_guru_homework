import os
import my_practice_form

class AutomationPracticeFormTestSuite:
    def __init__(self):
        self.automation_practice_form = my_practice_form.PracticeForm ("https://qa-guru.github.io/one-page-form/automation-practice-form.html")

    def setup(self):
        self.automation_practice_form.setup()
        self.tmp_file_name = self._create_tmp_file()

    def _create_tmp_file(self):
        file_path = os.path.abspath('test_file.jpg')
        with open(file_path, 'w') as file:
            file.write("Test")
        return file_path
    
    def test_form_positive01(self):
        self.automation_practice_form.fill_in_form(self.tmp_file_name, "Anna","Cica", "anna@example.com", "Female","0987654321",("2000", "5", "22"),("Maths", "English"), ("Reading", "Music"), "г. Красноярск, ул. Ленинский проспект, д 10", "NCR",  "Noida")
        self.automation_practice_form.assert_form(self.tmp_file_name, "Anna","Cica", "anna@example.com", "Female","0987654321",("2000", "5", "22"),("Maths", "English"), ("Reading", "Music"), "г. Красноярск, ул. Ленинский проспект, д 10", "NCR",  "Noida")

    def test_form_positive02(self):
        self.automation_practice_form.fill_in_form(self.tmp_file_name, "Dmitry","Bugaev", "bugaev@example.com", "Male","1234567890",("1988", "4", "22"),("Maths", "English"), ("Sports", "Music"), "г. Санкт-Петербург, ул. Невский проспект, д 101", "Haryana",  "Panipat")
        self.automation_practice_form.assert_form(self.tmp_file_name, "Dmitry","Bugaev", "bugaev@example.com", "Male","1234567890",("1988", "4", "22"),("Maths", "English"), ("Sports", "Music"), "г. Санкт-Петербург, ул. Невский проспект, д 101", "Haryana",  "Panipat")

    def tear_down(self):
        if os.path.exists(self.tmp_file_name):
            os.remove(self.tmp_file_name)
        self.automation_practice_form.tear_down()


test_suite = AutomationPracticeFormTestSuite()

try:
    test_suite.setup()
    test_suite.test_form_positive01()

finally:
    test_suite.tear_down() 

try:
    test_suite.setup()
    test_suite.test_form_positive02()

finally:
    test_suite.tear_down()