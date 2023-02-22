from .test_enum import WebBrowser
import test_login


# The link to the home website.
WEBSITE = 'http://www.python.org'
# The web_browser that would be used to test
WEB_BROWSER = WebBrowser.FIREFOX


def main():
    test_login(WEB_BROWSER)


if __name__ == '__main__':
    main()
