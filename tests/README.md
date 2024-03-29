# How to run the test
It is a good practice to be inside in the python environment for the project and you could check that you are inside the right python environment by doing:
```sh
pip -v
```
If it shows the directory to the current project that you are in the right directory. If you are not please refer to the installation guide at the root of the project.
## Running the test
To run all the pytest run:
```sh
pytest
```

To run a specific test or group of test write the command below, where `${test_mark}` is the test specific mark of the group/test:
```sh
pytest -m ${test_mark}
```
Please refer to the [test chapter](#Test) to find all test marks.
## Flags
- `--browser $(browser)` specifies with browser driver to use to run the test. The options that are available currently are `chrome`, `firefox`, `safari`, `edge` and `chromium`. If the flags is not given or an invalid value is given then it defaults to `firefox` because it is the best browser. Use example `pytest --browser chrome` to use the chrome webdriver.

- `--head $([0|1])` specifies that the test would run headless. Headless meaning that the webdriver would not show the UI while testing.
# Test
## test_login
- test_unsuccessfull_login
- test_successfull_login
- test_logout
