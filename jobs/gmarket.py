import json
import os
import time

from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from jobs.chrome import ChromeDriverLoader

LOGIN_URL = 'https://signinssl.gmarket.co.kr/login/login?url=https://www.gmarket.co.kr/'
ROULETTE_URL = 'https://promotion.gmarket.co.kr/Event/AttendRoulette_none.asp'
BENEFIT_URL = 'https://promotion.gmarket.co.kr/Event/pluszone.asp'


def run():
    with open(os.path.join(os.path.dirname(__file__), '..', 'config', '.gmarket.json')) as f:
        json_value = json.load(f)

    driver = ChromeDriverLoader().get_driver()
    driver.get(url=LOGIN_URL)

    try:
        # phase 1
        WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#btn_memberLogin'))
        )

        id_input_box = driver.find_element(By.CSS_SELECTOR, '#typeMemberInputId')
        id_input_box.send_keys(json_value['id'])

        password_input_box = driver.find_element(By.CSS_SELECTOR, '#typeMemberInputPassword')
        password_input_box.send_keys(json_value['password'])

        password_input_box.send_keys(Keys.ENTER)
        time.sleep(1)

        # phase 2
        driver.get(url=ROULETTE_URL)

        roulette_button = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#wrapper a.button_start'))
        )

        print(roulette_button)
        roulette_button.click()
        time.sleep(1)
        try:
            alert = driver.switch_to.alert
            print(alert.text)
            alert.accept()
        except NoAlertPresentException as e:
            pass

        # phase 3
        driver.get(url=BENEFIT_URL)
        time.sleep(1)

        WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.ID, 'footer'))
        )

        additional_benefits = driver.find_elements(By.CSS_SELECTOR, 'div.attendance_benefit a img')

        for benefit_button in additional_benefits:
            print(benefit_button)

            benefit_button.click()
            time.sleep(1)
            try:
                alert = driver.switch_to.alert
                print(alert.text)
                alert.accept()
            except NoAlertPresentException as e:
                pass

    except Exception as e:
        print(type(e))
        print(e)
    finally:
        print('done')
        driver.quit()


if __name__ == '__main__':
    run()
