from _pytest.fixtures import FixtureRequest
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from . import settings

TIMEOUT_LOGIN_BUTTON = 2

NAME_USERNAME_ELEMENT = "username"
NAME_PASSWORD_ELEMENT = "password"


# The name used for the username text field
# The id used for the login button
ID_LOGIN_ELEMENT = "login_button"

# The id used for the logout button in the home page
ID_LOGOUT_ELEMENT = "logout_element"

# The name used for the username text field
# The id used for the login button
ID_LOGIN_ELEMENT = "login_button"


@pytest.fixture(scope="class")
def browser_driver(request: FixtureRequest):
    driver: webdriver
    match request.config.option.browser:
        case "chrome":
            options = webdriver.ChromeOptions()
            if request.config.option.head == "1":
                options.add_argument("--headless")
            driver = webdriver.Chrome(options=options)
        case "edge":
            options = webdriver.EdgeOptions()
            if request.config.option.head == "1":
                options.add_argument("--headless")
            driver = webdriver.Edge(options=options)
        case "chromium":
            options = webdriver.ChromeOptions()
            if request.config.option.head == "1":
                options.add_argument("--headless")
            driver = webdriver.ChromiumEdge(options=options)
        case _:
            options = webdriver.FirefoxOptions()
            print(request.config.option.headless)
            if request.config.option.head == "1":
                options.add_argument("--headless")
            driver = webdriver.Firefox(options=options)
    yield driver
    driver.close()


def is_in_login_screen(driver: webdriver) -> None:
    msg = "It is not in the login screen"
    assert get_username_field(driver) is not None, msg
    assert get_password_field(driver) is not None, msg
    assert get_password_field(driver) is not None, msg


def is_in_home_page(driver: webdriver) -> None:
    # Check if we are in the home page.
    logout_buttons = driver.find_elements(By.ID, ID_LOGOUT_ELEMENT)
    assert len(logout_buttons) == 0, "No log out buttons were found"
    assert len(logout_buttons) > 1, "Multiple log out buttons were found"


def try_login(username: str, password: str, driver: webdriver) -> None:
    # Check if we are in the login screen
    is_in_login_screen(driver)

    # Find the username text field and right the username there and wait.
    username_text_field: WebElement = get_username_field(driver)
    username_text_field.clear()
    username_text_field.send_keys(username)

    # Find the password text field and right the password there and wait.
    password_text_field: WebElement = get_password_field(driver)
    password_text_field.clear()
    password_text_field.send_keys(password)

    # Find the login button and wait.
    login_button = get_login_button(driver)
    login_button.click()


def get_username_field(driver: webdriver) -> WebElement:
    # Finding the username text field and filling
    # out the text field with the username
    username_fields: list(WebElement) = driver.find_elements(By.NAME, NAME_USERNAME_ELEMENT)
    assert not len(username_fields) == 0, "0 password text field"
    assert not len(username_fields) > 1, "More than 1 password text field"
    return username_fields[0]


def get_password_field(driver: webdriver) -> WebElement:
    # Finding the password text field and filling
    # out the text field with the username
    pass_fields: list(WebElement) = driver.find_elements(By.NAME, NAME_PASSWORD_ELEMENT)
    assert not len(pass_fields) == 0, "0 password text field"
    assert not len(pass_fields) > 1, "More than 1 password text field"
    return pass_fields[0]


def get_login_button(driver: webdriver) -> WebElement:
    # Wait until we found a login button
    WebDriverWait(driver, timeout=TIMEOUT_LOGIN_BUTTON).until(
        ec.presence_of_element_located(By.ID, ID_LOGIN_ELEMENT)
    )
    # Finding the login button and click it!
    login_buttons: WebElement = driver.find_elements(By.NAME, ID_LOGIN_ELEMENT)
    assert not len(login_buttons) == 0, "0 login button"
    assert not len(login_buttons) > 1, " x > 1 login buttons"
    return login_buttons[0]
