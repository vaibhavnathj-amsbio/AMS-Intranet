import time

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse

from myDatabase.models import MasterCurrencies, Currencies

class TestmyDatabasePage(StaticLiveServerTestCase):
    databases = '__all__'

    def setUp(self):
        self.browser = webdriver.Chrome('./chromedriver.exe',)
        MasterCurrencies.objects.create(from_currency_id=4, to_currency_id=2, exchange_rate=1.4993)
        Currencies.objects.create(currencyid=4,descriptive='GBP')
        Currencies.objects.create(currencyid=2,descriptive='USD')

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

        from_curr = self.browser.find_element_by_xpath('//*[@id="testimonials"]/div/div[1]/div/div/table/tbody/tr[1]/td[1]').text
        to_curr = self.browser.find_element_by_xpath('//*[@id="testimonials"]/div/div[1]/div/div/table/tbody/tr[1]/td[2]').text
        rate = self.browser.find_element_by_xpath('//*[@id="testimonials"]/div/div[1]/div/div/table/tbody/tr[1]/td[3]').text        

        self.assertEquals(from_curr, 'GBP')
        self.assertEquals(to_curr, 'USD')
        self.assertEquals(rate, '1.4993')