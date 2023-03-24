import json
import os
import time

from selenium import webdriver
from selenium.common.exceptions import NoAlertPresentException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

LOGIN_URL = 'https://auth.danawa.com/login?url=http%3A%2F%2Fevent.danawa.com%2F'
EVENT_LIST_URL = 'https://event.danawa.com/event/lists?status=1&realType=3&pageNum='
ROULETTE_URL = 'https://promotion.gmarket.co.kr/Event/AttendRoulette_none.asp'
BENEFIT_URL = 'https://promotion.gmarket.co.kr/Event/pluszone.asp'


def run(path):
    with open(os.path.join(os.path.dirname(__file__), '..', 'config', '.danawa.json')) as f:
        json_value = json.load(f)

    driver = webdriver.Chrome(executable_path=path)
    driver.get(url=LOGIN_URL)

    try:
        # phase 1
        WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#danawa-member-login-loginButton'))
        )

        id_input_box = driver.find_element_by_css_selector('#danawa-member-login-input-id')
        id_input_box.send_keys(json_value['id'])

        password_input_box = driver.find_element_by_css_selector('#danawa-member-login-input-pwd')
        password_input_box.send_keys(json_value['password'])

        password_input_box.send_keys(Keys.ENTER)
        time.sleep(1)

        # phase 2

        driver.get(url=EVENT_LIST_URL + '1')

        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.co_paginate li.now'))
        )

        pagenation_buttons = driver.find_elements_by_css_selector('div.co_paginate li')

        lotto_url = ''
        roulette_urls = []

        for page in range(1, len(pagenation_buttons) + 1):
            driver.get(url=EVENT_LIST_URL + str(page))

            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div.co_paginate li.now'))
            )

            event_page_buttons = driver.find_elements_by_css_selector('table.list_tbl tbody tr td.title a.link_tit')

            for event_page_button in event_page_buttons:
                print(event_page_button.text)

                url = event_page_button.get_attribute('href')
                if '룰렛' in event_page_button.text:
                    roulette_urls.append(url)
                elif '로또' in event_page_button.text:
                    lotto_url = url
                else:
                    print(f'[INFO] 미분류 이벤트 : {event_page_button.text}/{url}')

        if lotto_url != '':
            driver.get(url=lotto_url)
            current_window_handle = driver.current_window_handle

            for _ in range(3):
                try:
                    WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, '#btn-auto-lotto-number'))
                    )

                    time.sleep(2)
                    driver.find_element_by_id('btn-auto-lotto-number').click()
                    time.sleep(2)
                    try:
                        alert = driver.switch_to.alert
                        print(alert.text)
                        alert.accept()
                    except NoAlertPresentException as e:
                        pass
                    driver.find_element_by_id('join-lotto-event').click()
                    time.sleep(2)
                    driver.switch_to.window(current_window_handle)

                    try:
                        alert = driver.switch_to.alert
                        print(alert.text)
                        alert.accept()
                        time.sleep(2)
                        driver.switch_to.window(current_window_handle)
                    except NoAlertPresentException as e:
                        if len(driver.find_elements(By.ID, 'btn-join-point-event')) == 0:
                            driver.find_element_by_id('agreePrivacy1').click()
                            driver.find_element_by_id('agreeAnotherPrivacy3').click()
                            driver.find_element_by_id('btn-privacy-agree-confirm').click()
                            time.sleep(2)
                            alert = driver.switch_to.alert
                            alert.accept()
                            time.sleep(2)
                            driver.find_element_by_id('btn-auto-lotto-number').click()
                            time.sleep(2)
                            driver.find_element_by_id('join-lotto-event').click()
                            time.sleep(2)
                            alert = driver.switch_to.alert
                            print(alert.text)
                            alert.accept()
                except TimeoutException as e:
                    driver.find_element_by_css_selector('span.win_prize.ico_win')

        for roulette_url in roulette_urls:

            print(roulette_url)
            driver.get(roulette_url)
            current_window_handle = driver.current_window_handle

            roulette_join_button = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#roulette-event-join'))
            )
            driver.switch_to.window(current_window_handle)

            roulette_join_count = 0
            while roulette_join_count < 3:
                try:
                    roulette_join_button.click()
                    time.sleep(2)
                    alert = driver.switch_to.alert
                    print(alert.text)
                    alert.accept()
                    roulette_join_count = roulette_join_count + 1
                except NoAlertPresentException as e:
                    if len(driver.find_elements(By.ID, 'btn-join-point-event')) > 0:
                        roulette_join_count = 3
                        continue

                    driver.find_element_by_id('agreePrivacy1').click()
                    driver.find_element_by_id('agreeAnotherPrivacy3').click()
                    driver.find_element_by_id('btn-privacy-agree-confirm').click()
                    time.sleep(2)
                    pass

        # print(pagenation_button)
        # pagenation_button.click()
        # time.sleep(1)
        # try:
        #     alert = driver.switch_to.alert
        #     print(alert.text)
        #     alert.accept()
        # except NoAlertPresentException as e:
        #     pass
        #
        # # phase 3
        # driver.get(url=BENEFIT_URL)
        # time.sleep(1)
        #
        # WebDriverWait(driver, 3).until(
        #     EC.presence_of_element_located((By.ID, 'footer'))
        # )
        #
        # additional_benefits = driver.find_elements_by_css_selector('div.attendance_benefit a')
        #
        # for benefit_button in additional_benefits:
        #     print(benefit_button)
        #
        #     benefit_button.click()
        #     time.sleep(1)
        #     try:
        #         alert = driver.switch_to.alert
        #         print(alert.text)
        #         alert.accept()
        #     except NoAlertPresentException as e:
        #         pass

    except Exception as e:
        print(type(e))
        print(e)
    finally:
        print('done')
        driver.quit()


if __name__ == '__main__':
    run(os.path.join(os.path.dirname(__file__), '..', 'chromedriver'))
