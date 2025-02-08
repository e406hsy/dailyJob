import datetime as dt
import json
import os
import time

from selenium.common.exceptions import NoAlertPresentException, TimeoutException, NoSuchElementException, \
    ElementClickInterceptedException, ElementNotInteractableException, UnexpectedAlertPresentException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from jobs.chrome import ChromeDriverLoader

LOGIN_URL = 'https://auth.danawa.com/login?url=http%3A%2F%2Fevent.danawa.com%2F'
EVENT_LIST_URL = 'https://event.danawa.com/event/lists?status=1&realType=3'
ROULETTE_URL = 'https://promotion.gmarket.co.kr/Event/AttendRoulette_none.asp'
BENEFIT_URL = 'https://promotion.gmarket.co.kr/Event/pluszone.asp'


# TODO: refactoring using OOP

def run():
    with open(os.path.join(os.path.dirname(__file__), '..', 'config', '.danawa.json')) as f:
        json_value = json.load(f)

    driver = ChromeDriverLoader().get_driver()
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

        today = dt.date.today()
        start = (today - dt.timedelta(days=90)).strftime('%Y.%m.%d')
        end = (today + dt.timedelta(days=90)).strftime('%Y.%m.%d')
        event_list_full_url = EVENT_LIST_URL + '&eventStartDate=' + start + '&eventEndDate=' + end + '&pageNum='
        driver.get(url=event_list_full_url + '1')

        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.co_paginate li.now'))
        )

        pagenation_buttons = driver.find_elements(by=By.CSS_SELECTOR, value='div.co_paginate li')

        lotto_url = ''
        roulette_urls = []
        croc_urls = []

        for page in range(1, len(pagenation_buttons) + 1):
            driver.get(url=event_list_full_url + str(page))

            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div.co_paginate li.now'))
            )

            event_page_buttons = driver.find_elements(by=By.CSS_SELECTOR,
                                                      value='table.list_tbl tbody tr td.title a.link_tit')

            for event_page_button in event_page_buttons:
                print(event_page_button.text)

                url = event_page_button.get_attribute('href')
                if '룰렛' in event_page_button.text:
                    roulette_urls.append(url)
                elif '로또' in event_page_button.text:
                    lotto_url = url
                elif '악어' in event_page_button.text:
                    croc_urls.append(url)
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
                    driver.find_element(by=By.ID, value='btn-auto-lotto-number').click()
                    time.sleep(2)
                    try:
                        alert = driver.switch_to.alert
                        print(alert.text)
                        alert.accept()
                    except NoAlertPresentException as e:
                        pass
                    driver.find_element(by=By.ID, value='join-lotto-event').click()
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
                            driver.find_element(by=By.ID, value='agreePrivacy1').click()
                            driver.find_element(by=By.ID, value='agreeAnotherPrivacy3').click()
                            driver.find_element(by=By.ID, value='agreedParticipationRestriction5').click()
                            driver.find_element(by=By.ID, value='btn-privacy-agree-confirm').click()
                            time.sleep(2)
                            alert = driver.switch_to.alert
                            alert.accept()
                            time.sleep(2)
                            driver.find_element(by=By.ID, value='btn-auto-lotto-number').click()
                            time.sleep(2)
                            driver.find_element(by=By.ID, value='join-lotto-event').click()
                            time.sleep(2)
                            alert = driver.switch_to.alert
                            print(alert.text)
                            alert.accept()
                except TimeoutException as e:
                    pass
                    # driver.find_element_by_css_selector('span.win_prize.ico_win')

        for roulette_url in roulette_urls:

            print(roulette_url)
            driver.get(roulette_url)
            current_window_handle = driver.current_window_handle

            try:
                roulette_join_button = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '#roulette-event-join'))
                )
            except TimeoutException as e:
                print('[DEBUG]failed to find roulette button on page ' + roulette_url)
                croc_urls.append(roulette_url)
                continue

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

                    try:
                        driver.find_element(by=By.ID, value='agreePrivacy1').click()
                        driver.find_element(by=By.ID, value='agreeAnotherPrivacy3').click()
                        driver.find_element(by=By.ID, value='agreedParticipationRestriction5').click()
                        driver.find_element(by=By.ID, value='btn-privacy-agree-confirm').click()
                        time.sleep(2)
                    except NoSuchElementException as e:
                        print('[ERROR] no privacy check button found.')
                        break

        for _ in [0, 1]:
            for croc_url in croc_urls:

                print(croc_url)
                driver.get(croc_url)
                current_window_handle = driver.current_window_handle

                try:
                    roulette_join_button = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, '.imgBtn.btn-game-page'))
                    )
                except TimeoutException as e:
                    print('[WARN] failed to find croc button on page ' + croc_url)
                    croc_urls.append(croc_url)
                    continue

                driver.switch_to.window(current_window_handle)
                try:
                    roulette_join_button.click()
                    time.sleep(2)
                    driver.find_element(by=By.ID, value='agreePrivacy1').click()
                    driver.find_element(by=By.ID, value='agreeAnotherPrivacy3').click()
                    driver.find_element(by=By.ID, value='agreedParticipationRestriction5').click()
                    driver.find_element(by=By.ID, value='btn-privacy-agree-confirm').click()
                    time.sleep(2)
                    alert = driver.switch_to.alert
                    print(alert.text)
                    alert.accept()
                    time.sleep(2)
                    driver.find_element(by=By.CSS_SELECTOR, value='.imgBtn.btn-game-page').click()
                except UnexpectedAlertPresentException as e:
                    print('[WARN] Unexpected alert ' + e.alert_text)
                    pass
                except NoSuchElementException as e:
                    pass

                for i in range(0, 3):
                    try:
                        driver.find_element(by=By.ID, value='tooth' + str(i)).click()
                        time.sleep(2)
                    except ElementClickInterceptedException as e:
                        pass
                    except ElementNotInteractableException as e:
                        pass

    except Exception as e:
        print(type(e))
        print(e)
    finally:
        print('done')
        driver.quit()


if __name__ == '__main__':
    run()
