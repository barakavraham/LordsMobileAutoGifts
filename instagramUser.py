from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import getpass


def instagram_login(driver, user=False, password=False):
    print("\nEntering to instagram login page...")
    driver.get("https://www.instagram.com/accounts/login")
    for i in range(3):
        try:
            username_input = WebDriverWait(driver, 8).until(
                EC.presence_of_element_located((By.NAME, "username")))
            password_input = WebDriverWait(driver, 8).until(
                EC.presence_of_element_located((By.NAME, "password")))
            submit = WebDriverWait(driver, 8).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Log In')]")))
            print("page loaded!\n")
            break
        except:
            if i == 2:
                print("Couldn't load the page, tring to connect lordsmobile without account!\n")
            else:
                print("Page failed to load, tring again!")
                continue
        return (False, False, False)

    while True:
        if not user or not password:
            user = input('Instgram username: ')
            password = getpass.getpass('Instgram password: ')
        username_input.send_keys(user)
        password_input.send_keys(password)
        submit.click()
        try:
            print('Login in... please wait')
            errorMessage = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "_6q-tv")))
            print("Login successful!")
            break
        except:
            pass

        print(driver.find_element_by_id("slfErrorAlert").text + '\n')
        if input('*NOT RECOMMANDED* Do you want to try continue without login? (y/n): ') == 'y':
            print('')
            return (False, False, False)
        for char in range(len(user)):
            username_input.send_keys(Keys.BACK_SPACE)
        for char in range(len(password)):
            password_input.send_keys(Keys.BACK_SPACE)
        user, password = (False, False)
    return (True, user, password)

def instagram_logout(driver):
    print("Trying to logout from instagram...")
    driver.get("https://www.instagram.com/accounts/logout")
    print("Logout successful!\n")
    driver.get("https://www.instagram.com/lordsmobile")
    return False