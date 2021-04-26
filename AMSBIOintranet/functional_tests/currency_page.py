import time

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse


class TestmyDatabasePage(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Chrome('./chromedriver.exe',)

    def tearDown(self):
        self.browser.close()

    def test_currency_page(self):
        self.browser.maximize_window()
        self.browser.get(self.live_server_url)

        action = ActionChains(self.browser)

        firstLevelMenu = self.browser.find_element_by_id("database_drop_down")
        action.move_to_element(firstLevelMenu).perform()
        secondLevelMenu = self.browser.find_element_by_id("currency_ex")
        action.move_to_element(secondLevelMenu).perform()
        secondLevelMenu.click()
        time.sleep(2)

        from_curr = self.browser.find_element_by_xpath('//*[@id="testimonials"]/div/div[1]/div/div/table/tbody/tr[1]/td[1]').text
        to_curr = self.browser.find_element_by_xpath('//*[@id="testimonials"]/div/div[1]/div/div/table/tbody/tr[1]/td[2]').text

        self.assertEquals(from_curr, 'GBP')
        self.assertEquals(to_curr, 'USD')