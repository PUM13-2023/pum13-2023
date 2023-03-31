"""Test for selenium and pytest compatability.

This module is for testing that Selenium and pytest works on your
system.

This module is run using:
pytest -k youtube
"""
from time import sleep

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement

YOUTUBE = "https://www.youtube.com/"


class TestSeleniumPytest:
    """Class that runs selenium and pytest test."""

    @pytest.fixture(scope="session")
    def browser_driver(self, request):
        """Match what webdriver Selenium should use."""
        match request.config.option.browser:
            case "chrome":
                driver = webdriver.Chrome()
            case "safari":
                driver = webdriver.Safari()
            case "edge":
                driver = webdriver.Edge()
            case "chromium":
                driver = webdriver.ChromiumEdge()
            case _:
                driver = webdriver.Firefox()
        yield driver
        driver.close()

    @pytest.mark.youtube
    @pytest.mark.usefixtures("browser_driver")
    def test_play_youtube_video(self, browser_driver):
        """Plays a youtube video testing Selenium functions."""
        browser_driver.get(YOUTUBE)
        sleep(1)
        accept_all_button = browser_driver.find_elements(
            By.XPATH,
            "/html/body/ytd-app/ytd-consent-bump-v2-lightbox/tp-yt-paper-"
            "dialog/div[4]/div[2]/div[6]/div[1]/ytd-button-renderer[2]/yt"
            "-button-shape/button",
        )[0]

        accept_all_button.click()
        sleep(1)

        search_bar: WebElement = browser_driver.find_elements(By.XPATH, '//input[@id="search"]')[0]
        search_bar.clear()
        search_bar.send_keys("Rick Astley - " "Never Gonna Give You Up (Official Music Video)")
        sleep(1)

        search_button: WebElement = browser_driver.find_elements(
            By.XPATH, '//*[@id="search-icon-legacy"]'
        )[0]
        search_button.click()
        sleep(1)

        rick_astley_video: WebElement = browser_driver.find_elements(
            By.XPATH,
            "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-search/div[1]/"
            "ytd-two-column-search-results-renderer/div/ytd-section-list-"
            "renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-video-"
            "renderer[1]/div[1]/div",
        )[0]
        rick_astley_video.click()
        sleep(7)

        skip_add_button: WebElement = browser_driver.find_elements(
            By.XPATH,
            "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]"
            "/div[1]/div/div[1]/div[2]/div/div/ytd-player/div/div/div[17]/div/"
            "div[3]/div/div[2]/span/button",
        )[0]
        skip_add_button.click()
        sleep(1)
        video_player: WebElement = browser_driver.find_elements(
            By.XPATH,
            "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/"
            "div[5]/div[1]/div/div[1]/div[2]/div/div/ytd-player/div/div/"
            "div[1]/video",
        )[0]
        video_player.send_keys("f")
        sleep(3)
        video_player.send_keys(Keys.SPACE)
        sleep(1)
        video_player.send_keys(Keys.SPACE)
        sleep(10)
