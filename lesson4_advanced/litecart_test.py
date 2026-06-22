from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.accept_insecure_certs = True

driver = webdriver.Chrome(options=options)

try:
    driver.get("https://litecart.stqa.ru/en/")
    driver.maximize_window()
    print("Сайт открылся успешно!")
    print(f"Заголовок страницы: {driver.title}")

finally:
    driver.quit()