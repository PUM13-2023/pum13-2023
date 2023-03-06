import pytest

from .helper_test_functions import *

def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="")
    parser.addoption("--speedmult", action="store", default="1")
    parser.addoption("--head", action="store", default="1")
