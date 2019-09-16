from instagramUser import instagram_login, instagram_logout
from lordsUsers import users
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime
import random
import re
import requests
import selenium.webdriver.support.ui as ui
import time

user_login, insta_user, insta_password = (False, False, False)
options = webdriver.ChromeOptions()
# options.add_argument('headless')
options.add_argument('log-level=3')
driver = webdriver.Chrome(options=options, executable_path=r'C:/Program Files (x86)/Google/Chrome/Application/chromedriver.exe')

if input('\n*NOT RECOMMANDED* Do you want to start the program without login to Instagram? (y/n): ') == 'n':
    user_login, insta_user, insta_password = instagram_login(driver)
driver.get("https://www.instagram.com/lordsmobile")
print("\nStarting program...\n")
div = driver.find_elements_by_class_name('v1Nh3')
refreshCount = 0

while True:
    linknum = 1
    refreshCount += 1
    print('----------------------------------------------')
    print(f'{datetime.datetime.now().strftime("%H:%M:%S")}\n-- Refresh {refreshCount} --\n\npage is loading...')
    with open("posts.txt", "r") as fd:
        links = fd.read().splitlines()
    posts = open('posts.txt', 'a')
    driver.get("https://www.instagram.com/lordsmobile/")
    try:
        WebDriverWait(driver, 8).until(
            EC.presence_of_element_located((By.CLASS_NAME, "rhpdm")))
        print('Page loaded successfully!\n')
    except:
        print('Error: Page not found\n')
        if user_login:
            user_login = instagram_logout(driver)
        else:
            user_login, insta_user, insta_password = instagram_login(driver, insta_user, insta_password)
        print(f'-- loop ended --\n{datetime.datetime.now().strftime("%H:%M:%S")}')
        print('----------------------------------------------')
        continue
    div = driver.find_elements_by_class_name('v1Nh3')
    livePosts = [element.find_element_by_css_selector('a').get_attribute('href') for element in div]
    for link in livePosts:
        if link not in links:
            posts.write(link + '\n')
            driver.get(link)
            print(f'// Link {linknum} //\nLINK ADDRESS: {link}\n')
            linknum += 1
            r = requests.get(link)
            try:
                WebDriverWait(driver, 8).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "glyphsSpriteShare__outline__24__grey_9")))
                code = re.findall(r"(?<=Code:).*?(?= -)", r.content.decode('utf-8'))[0]
            except:
                print('No code found on that link\n')
                continue
            code = code.replace(' ', '')
            for user in users:
                driver.get("https://lordsmobile.igg.com/event/cdkey/")
                id_input = driver.find_element_by_id('iggid')
                code_input = driver.find_element_by_id('cdkey')
                submit = driver.find_element_by_id('submit')
                id_input.send_keys(user["IGGID"])
                code_input.send_keys(code)
                submit.click()
                try:
                    message = WebDriverWait(driver, 4).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "msg_con")))
                    print(f'{user["name"]}: {message.text}')
                except:
                    print(f'{user["name"]}: Unknown error')
            print('')
    posts.close()
    print(f'-- loop ended --\n{datetime.datetime.now().strftime("%H:%M:%S")}\n----------------------------------------------')
    time.sleep(random.randint(60,90))

