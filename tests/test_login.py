from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from time import sleep
from .test_enum import WebBrowser

import pytest


class LoginSettings():
    START_PAGE_URL = 'https://www.google.com/'
    WEB_BROWSER = WebBrowser.FIREFOX

    # The name used for the username text field
    NAME_USERNAME_ELEMENT = 'username'

    # The name used for the password text field
    NAME_PASSWORD_ELEMENT = 'password'

    # The id used for the login button
    ID_LOGIN_ELEMENT = 'login_button'

    # The id used for the pop up element
    ID_POP_UP_ELEMENT = 'popup_login_error'

    # The id used for the logout button in the home page
    ID_LOGOUT_ELEMENT = 'logout_element'

    # Login credentials for the valid test user
    USERS_USERNAME = 'valid_user'
    USERS_PASSWORD = 'valid_user_password'
    WRONG_USERNAME = 'not_valid_user'
    WRONG_PASSWORD = 'not_valid_user_password'

    SLEEP_TIME_USERNAME_FIELD = 1
    SLEEP_TIME_PASSWORD_FIELD = 1
    SLEEP_TIME_LOGIN_BUTTON = 5
    SLEEP_TIME_REFRESH = 5


@pytest.fixture
def website_url():
    return LoginSettings.START_PAGE_URL


@pytest.fixture
def web_browser():
    return LoginSettings.WEB_BROWSER


@pytest.fixture
def browser_driver(web_browser, website_url):
    match web_browser:
        case WebBrowser.FIREFOX:
            driver = webdriver.Firefox()
        case WebBrowser.CHROME:
            driver = webdriver.Chrome()
    driver.get(website_url)
    return driver


def test_unsuccessful_login(browser_driver):
    username_text_field_exist = check_username_text_field(browser_driver)
    if (not username_text_field_exist):
        browser_driver.close()
    assert username_text_field_exist, "There is no username text field"
    # Try logging in with wrong password and username
    if not try_login(LoginSettings.WRONG_USERNAME,
                     LoginSettings.WRONG_PASSWORD,
                     browser_driver):
        return
    check_login_error_pop_up(browser_driver)

    # Try logging in with wrong password
    try_login(LoginSettings.USERS_USERNAME,
              LoginSettings.WRONG_PASSWORD,
              browser_driver)
    check_login_error_pop_up(browser_driver)

    # Try logging in with wrong username
    try_login(LoginSettings.WRONG_USERNAME,
              LoginSettings.USERS_PASSWORD,
              browser_driver)
    check_login_error_pop_up(browser_driver)


# def test_successfull_login(browser_driver):
#     try_login(LoginSettings.USERS_USERNAME,
#               LoginSettings.USERS_PASSWORD,
#               browser_driver)

#     # Check that we are still in the homepage after login in
#     assert (is_in_home_page(browser_driver))

#     # Check that we are still  in the homepage after
#     # refreshing in the login page.
#     browser_driver.refresh()
#     assert (is_in_home_page(browser_driver))

#     browser_driver.close()


# def test_logout(browser_driver):
#     sleep(5)
#     # try_login(LoginSettings.USERS_USERNAME,
#     #           LoginSettings.USERS_PASSWORD,
#     #           browser_driver)
#     # Check that we are still in the homepage after login in
#     # assert (is_in_home_page(browser_driver))

#     browser_driver.close()

def check_username_text_field(driver: webdriver):
    username_text_field_candidates: list(WebElement) = driver.find_elements(
        By.NAME, LoginSettings.NAME_USERNAME_ELEMENT)
    n_username_text = len(username_text_field_candidates)
    return n_username_text == 1


def try_login(username, password, driver: webdriver) -> bool:
    # Finding the username text field and filling out the text field with
    # the username
    username_text_field_candidates: list(WebElement) = driver.find_elements(
        By.NAME, LoginSettings.NAME_USERNAME_ELEMENT)
    n_username_text = len(username_text_field_candidates)
    print(n_username_text)
    if (n_username_text != 1):
        driver.close()
        n_username_text = len(username_text_field_candidates)
        assert n_username_text != 1, "Could not find the username text field"
        return False
    username_text_field: WebElement = username_text_field_candidates[0]
    username_text_field.clear()
    username_text_field.send_keys(username)
    sleep(LoginSettings.SLEEP_TIME_USERNAME_FIELD)

    # Finding the password text field and filling out the text field with
    # the username
    password_text_field_candidates: list(WebElement) = driver.find_elements(
        By.NAME, LoginSettings.NAME_PASSWORD_ELEMENT)
    if (len(password_text_field_candidates) != 1):
        driver.close()
        assert (len(username_text_field_candidates) != 1)
    password_text_field: WebElement = password_text_field_candidates[0]
    password_text_field.clear()
    password_text_field.send_keys(password)
    sleep(LoginSettings.SLEEP_TIME_PASSWORD_FIELD)

    # Finding the login button and click it!
    login_button: WebElement = driver.find_element(
        By.NAME, LoginSettings.ID_LOGIN_ELEMENT)
    assert (login_button is not None)
    login_button.click()
    sleep(LoginSettings.SLEEP_TIME_LOGIN_BUTTON)


def check_login_error_pop_up(driver: webdriver) -> None:
    # Check if the login error pop up exist and then refresh the site and
    # check that it does not exist.
    pop_up_element: WebElement = driver.find_element(
        By.ID, LoginSettings.ID_POP_UP_ELEMENT)
    assert (pop_up_element is not None)
    driver.refresh()
    sleep(LoginSettings.SLEEP_TIME_REFRESH)
    pop_up_element: WebElement = driver.find_element(
        By.ID, LoginSettings.ID_POP_UP_ELEMENT)
    assert (pop_up_element is None)


def is_in_home_page(driver: webdriver) -> None:
    # Check if we are in the home page.
    in_home_page: bool = driver.find_element(
        By.ID, LoginSettings.ID_LOGOUT_ELEMENT) is not None
    return in_home_page
