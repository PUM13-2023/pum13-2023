from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from enum import Enum


class WebBrowser(Enum):
    FIREFOX = 1
    CHROME = 2


# The link toi the home website.
WEBSITE = 'http://www.python.org'
WEB_BROWSER = WebBrowser.FIREFOX


def test_login(web_browser: WebBrowser):
    match web_browser:
        case WebBrowser.FIREFOX:
            print('==============================')
            print('Testing login on firefox')

            driver = webdriver.Firefox()
        case WebBrowser.CHROME:
            print('==============================')
            print('Testing login on chrome')
            driver = webdriver.Safari()
    driver.get(WEBSITE)

    title_test = 'Python' in driver.title
    assert title_test
    if not title_test:
        print('Result: FAIL')
        print('==============================')
        driver.close()

    elem = driver.find_element(By.NAME, 'q')
    elem.clear()
    elem.send_keys('pycon')
    elem.send_keys(Keys.RETURN)

    assert 'No results found.' not in driver.page_source
    print('Result: PASS')
    print('==============================')
    driver.close()


def main():
    test_login(WEB_BROWSER)


if __name__ == '__main__':
    main()
