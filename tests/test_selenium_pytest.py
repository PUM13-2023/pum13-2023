from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.keys import Keys
from time import sleep
from .test_enum import WebBrowser

import pytest


class Settings():
    YOUTUBE = 'https://www.youtube.com/'
    WEB_BROWSER = WebBrowser.FIREFOX


class TestSeleniumPytest():

    @pytest.fixture
    def browser_driver(self):
        match Settings.WEB_BROWSER:
            case WebBrowser.FIREFOX:
                self.driver = webdriver.Firefox()
            case WebBrowser.CHROME:
                self.driver = webdriver.Chrome()
        yield
        self.driver.close()

    @pytest.mark.youtube
    @pytest.mark.usefixtures('browser_driver')
    def test_play_youtube_video(self):
        self.driver.get(Settings.YOUTUBE)
        sleep(1)
        accept_all_button = self.driver.find_elements(
            By.XPATH, '/html/body/ytd-app/ytd-consent-bump-v2-lightbox/tp-yt-paper-dialog/div[4]/div[2]/div[6]/div[1]/ytd-button-renderer[2]/yt-button-shape/button')[0]

        accept_all_button.click()
        sleep(1)

        search_bar: WebElement = self.driver.find_elements(
            By.XPATH, '//input[@id="search"]')[0]
        search_bar.clear()
        search_bar.send_keys('Rick Astley - Never Gonna Give You Up (Official Music Video)')
        sleep(1)

        search_button: WebElement = self.driver.find_elements(
            By.XPATH, '//*[@id="search-icon-legacy"]'
        )[0]
        search_button.click()
        sleep(1)

        rick_astley_video: WebElement = self.driver.find_elements(
            By.XPATH, '/html/body/ytd-app/div[1]/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-video-renderer[1]/div[1]/div'
        )[0]
        rick_astley_video.click()
        sleep(7) 

        skip_add_button: WebElement = self.driver.find_elements(By.XPATH,
        '/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[1]/div[2]/div/div/ytd-player/div/div/div[17]/div/div[3]/div/div[2]/span/button')[0]
        skip_add_button.click()
        sleep(1)
        video_player: WebElement = self.driver.find_elements(By.XPATH,
                                                             '/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[1]/div[2]/div/div/ytd-player/div/div/div[1]/video')[0]
        video_player.send_keys('f')
        sleep(3)
        video_player.send_keys(Keys.SPACE)
        sleep(1)
        video_player.send_keys(Keys.SPACE)
        sleep(10)

