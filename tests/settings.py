"""Settings constant."""
from selenium import webdriver

# Server settings
PORT = 8000
HOST = "127.0.0.1"
URL = f"http://{HOST}:{str(PORT)}"
SERVER_STARTUP_WAIT = 3

# Normally used constants
START_PAGE_URL = f"{URL}/login/"
HOME_PAGE_URL = f"{URL}/"
DASHBOARD_PAGE_URL = f"{URL}/dashboards"
SHARED_DASHBOARDS_PAGE_URL = f"{URL}/shared-dashboards"

USERS_USERNAME = "admin"
USERS_PASSWORD = "admin"

NORMAL_TIMEOUT = 1

# Navbar button id:s
HOME_BUTTON_NAV = "home_button_nav"
DASHBOARD_BUTTON_NAV = "dashboard_button_nav"

# Constants specifically for test_login

# Type aliases
DriverType = (
    webdriver.Chrome
    | webdriver.Firefox
    | webdriver.Safari
    | webdriver.Edge
    | webdriver.ChromiumEdge
)
