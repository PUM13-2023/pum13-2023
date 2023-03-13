from _pytest.fixtures import FixtureRequest
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import TimeoutException, WebDriverWait

from . import settings

TIMEOUT_BUTTON = 2
TIMEOUT_TEXTFIELD = 2

ID_USERNAME_ELEMENT = "username_textfield"
ID_PASSWORD_ELEMENT = "password_textfield"


# The name used for the username text field
# The id used for the login button
ID_LOGIN_BUTTON_ELEMENT = "login_button"

# The id used for the logout button in the home page
ID_LOGOUT_ELEMENT = "logout_element"


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
    assert get_element_by_id(ID_USERNAME_ELEMENT, driver) is not None, msg
    assert get_element_by_id(ID_PASSWORD_ELEMENT, driver) is not None, msg


def is_in_home_page(driver: webdriver) -> None:
    # Check if there is a log out button
    assert get_element_by_id(ID_LOGOUT_ELEMENT, driver) is not None


def try_login(username: str, password: str, driver: webdriver) -> None:
    # Find the username text field and right the username there and wait.
    username_text_field: WebElement = get_element_by_id(ID_USERNAME_ELEMENT, driver)
    username_text_field.clear()
    username_text_field.send_keys(username)

    # Find the password text field and right the password there and wait.
    password_text_field: WebElement = get_element_by_id(ID_PASSWORD_ELEMENT, driver)
    password_text_field.clear()
    password_text_field.send_keys(password)

    # Find the login button and wait.
    login_button = get_element_by_id(ID_LOGIN_BUTTON_ELEMENT, driver)
    login_button.click()


def get_element_by_id(element_id: str, driver: webdriver) -> WebElement:
    msg_not_found = "The element with the element id {" + element_id + "} was not found"
    msg_found_multiple = "There was multiple element with the id {" + element_id + "} found."

    # Wait until we found a button with the given id
    WebDriverWait(driver, timeout=settings.NORMAL_TIMEOUT).until(
        ec.presence_of_element_located((By.ID, element_id))
    )

    # Finding the button, check that we only found one and click it!
    elements: WebElement = driver.find_elements(By.NAME, element_id)
    assert not len(elements) == 0, msg_not_found
    assert not len(elements) > 1, msg_found_multiple
    return elements[0]
