from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from time import sleep
from enum import Enum

from .test_enum import WebBrowser


class LoginSettings(Enum):
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


def test_login(website: str, web_browser: WebBrowser) -> None:
    # Starting up the browser
    match web_browser:
        case WebBrowser.FIREFOX:
            driver = webdriver.Firefox()
        case WebBrowser.CHROME:
            driver = webdriver.Chrome()
    driver.get(website)

    try_unsuccessful_login(driver)
    driver.refresh()
    if try_successfull_login(driver):
        try_logout(driver)
    else:
        print("The login was not successfull so we are not running the logout test")

    driver.close()


def try_unsuccessful_login(driver: webdriver) -> None:
    # Try logging in with wrong password and username
    try_login(LoginSettings.WRONG_USERNAME,
              LoginSettings.WRONG_PASSWORD,
              driver)
    check_login_error_pop_up(driver)

    # Try logging in with wrong password
    try_login(LoginSettings.USERS_USERNAME,
              LoginSettings.WRONG_PASSWORD,
              driver)
    check_login_error_pop_up(driver)

    # Try logging in with wrong username
    try_login(LoginSettings.WRONG_USERNAME,
              LoginSettings.USERS_PASSWORD,
              driver)
    check_login_error_pop_up(driver)


def try_login(username, password, driver: webdriver) -> None:
    # Finding the username text field and filling out the text field with
    # the username
    username_text_field: WebElement = driver.find_element(
        By.NAME, LoginSettings.ID_USERNAME_ELEMENT)
    assert (username_text_field is not None)
    username_text_field.clear()
    username_text_field.send_keys(username)
    sleep(LoginSettings.SLEEP_TIME_USERNAME_FIELD)

    # Finding the password text field and filling out the text field with
    # the username
    password_text_field: WebElement = driver.find_element(
        By.NAME, LoginSettings.ID_PASSWORD_ELEMENT)
    assert (password_text_field is not None)
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


def try_successfull_login(driver: webdriver) -> bool:
    try_login(LoginSettings.USERS_USERNAME,
              LoginSettings.USERS_PASSWORD,
              driver)

    # Check that we are still in the homepage after login in
    is_in_home_page(driver)
    assert (is_in_home_page)

    # Check that we are still  in the homepage after refreshing in the login page.
    driver.refresh()
    in_home_page: bool = is_in_home_page(driver)
    assert (is_in_home_page)

    return in_home_page


def try_logout(driver: webdriver) -> None:
