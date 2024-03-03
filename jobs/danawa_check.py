import json
import os
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

LOGIN_URL = 'https://auth.danawa.com/login?url=http%3A%2F%2Fevent.danawa.com%2F'
ATTENDANCE_CHECK_URL = 'https://dpg.danawa.com/mobile/attendance/main'

# TODO: refactoring using OOP

def run():
    with open(os.path.join(os.path.dirname(__file__), '..', 'config', '.danawa.json')) as f:
        json_value = json.load(f)

    opts = Options()
    opts.add_argument("user-agent=Mozilla/5.0 (Linux; Android 11; SAMSUNG SM-G973U) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/14.2 Chrome/87.0.4280.141 Mobile Safari/537.36")

    driver = webdriver.Chrome(options=opts )
    driver.get(url=LOGIN_URL)

    try:
        # phase 1
        WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#danawa-member-login-loginButton'))
        )

        id_input_box = driver.find_element(by=By.CSS_SELECTOR, value='#danawa-member-login-input-id')
        id_input_box.send_keys(json_value['id'])

        password_input_box = driver.find_element(by=By.CSS_SELECTOR, value='#danawa-member-login-input-pwd')
        password_input_box.send_keys(json_value['password'])

        password_input_box.send_keys(Keys.ENTER)
        time.sleep(1)

        # phase 2

        driver.get(url=ATTENDANCE_CHECK_URL)

        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#danawa-dpg-mobile-attendance-main-button-excute'))
        )

        attend_button = driver.find_element(by=By.CSS_SELECTOR, value='#danawa-dpg-mobile-attendance-main-button-excute')

        attend_button.click()
        time.sleep(2)

    except Exception as e:
        print(type(e))
        print(e)
    finally:
        print('done')
        driver.quit()


if __name__ == '__main__':
    run()
