from selenium import webdriver
from selenium.webdriver.common.by import By

from .test_enum import WebBrowser

# The id used for the username text field
ID_USERNAME_ELEMENT = 'username'

# The id used for the password text field
ID_PASSWORD_ELEMENT = 'password'

# The id used for the login button
ID_LOGIN_ELEMENT = 'login_button'

# Login credentials for the test user
USERS_USERNAME = 'chris'
USERS_PASSWORD = 'qwerty'


def test_login(website: str, web_browser: WebBrowser):
    # Starting up the browser
    match web_browser:
        case WebBrowser.FIREFOX:
            print('==============================')
            print('Testing login on firefox')

            driver = webdriver.Firefox()
        case WebBrowser.CHROME:
            print('==============================')
            print('Testing login on chrome')
            driver = webdriver.Chrome()
    driver.get(website)

    # Finding the username text field and filling out the text field with
    # the username
    username_text_field = driver.find_element(By.NAME, ID_USERNAME_ELEMENT)
    username_text_field.clear()
    username_text_field.send_keys(USERS_USERNAME)

    password_text_field = driver.find_element(By.NAME, ID_PASSWORD_ELEMENT)
    password_text_field.clear()
    password_text_field.send_keys(USERS_PASSWORD)

    login_button = driver.find_element(By.NAME, ID_LOGIN_ELEMENT)
    login_button.click()

    driver.close()
