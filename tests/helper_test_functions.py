"""Helper functions for test."""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from . import settings

TIMEOUT_BUTTON = 2
TIMEOUT_TEXTFIELD = 2

ID_USERNAME_ELEMENT = "username"
ID_PASSWORD_ELEMENT = "password"


# The name used for the username text field
# The id used for the login button
ID_LOGIN_BUTTON_ELEMENT = "login_button"

# The id used for the logout button in the home page
ID_LOGOUT_ELEMENT = "logout_element"


def is_in_login_screen(driver: webdriver) -> None:
    """Check if the driver is currently at the login screen.

    This functions checks if the driver is in the login screen
    by checking if elements specific exist in the login screen.

    Args:
        driver (webdriver): The webdriver that would be checked.
    """
    msg = "It is not in the login screen"
    assert get_element_by_id(driver, ID_USERNAME_ELEMENT) is not None, msg
    assert get_element_by_id(driver, ID_PASSWORD_ELEMENT) is not None, msg


def is_in_home_page(driver: webdriver) -> None:
    """Check if the driver is currently at the home page.

    This functions checks if the driver is in the home page
    by checking if specific elements exist in the login
    screen.

    Args:
        driver (webdriver): The webdriver that would be checked.
    """
    print(driver.current_url)
    assert driver.current_url == settings.HOME_PAGE_URL
    # assert get_element_by_id(driver, ID_LOGOUT_ELEMENT) is not None


def try_login(driver: webdriver, username: str, password: str) -> None:
    """Try to login to the homepage.

    This functions tries to login to the home page.

    Args:
        username (str): The username of the user.
        password (str): The password of the user.
        driver (webdriver): The webdriver that would be used.
    """
    # Find the username text field and right the username
    # there and wait.
    username_text_field: WebElement = get_element_by_id(driver, ID_USERNAME_ELEMENT)
    username_text_field.clear()
    username_text_field.send_keys(username)

    # Find the password text field and right the password
    # there and wait.
    password_text_field: WebElement = get_element_by_id(driver, ID_PASSWORD_ELEMENT)
    password_text_field.clear()
    password_text_field.send_keys(password)

    # Find the login button and wait.
    login_button = get_element_by_id(driver, ID_LOGIN_BUTTON_ELEMENT)
    login_button.click()


def get_element_by_id(driver: webdriver, element_id: str) -> WebElement:
    """Get element by their id.

    This function would try to get the element by id. If the
    element does now show up after settings.NORMAL_TIMEOUT
    it will raise an error.

    Args:
        element_id (str): The element id.
        driver (webdriver): The driver that would be used.
    """
    # Wait until we found a button with the given id
    WebDriverWait(driver, timeout=settings.NORMAL_TIMEOUT).until(
        ec.presence_of_element_located((By.ID, element_id))
    )

    # Finding the button, check that we only found one and click it!
    element: WebElement = driver.find_element(By.ID, element_id)
    return element
