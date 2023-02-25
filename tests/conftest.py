

def pytest_addoption(parser):
    parser.addoption('--browser', action='store', default='')
    parser.addoption('--speedmult', action='store', default='1')
