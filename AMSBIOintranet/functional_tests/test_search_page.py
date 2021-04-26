import time

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse

from myDatabase.models import ProductRecords


class TestmyDatabasePage(StaticLiveServerTestCase):
    databases = '__all__'

    def setUp(self):
        self.browser = webdriver.Chrome('./chromedriver.exe',)
        ProductRecords.objects.create(product_code='RANDOM.AMS-value001', category_1=121, category_2=116)
        
    def tearDown(self):
        self.browser.close()

    def test_search_db_page(self):
        self.browser.maximize_window()
        self.browser.get(self.live_server_url)

        action = ActionChains(self.browser)

        firstLevelMenu = self.browser.find_element_by_id("database_drop_down")
        action.move_to_element(firstLevelMenu).perform()
        secondLevelMenu = self.browser.find_element_by_id("search_db")
        action.move_to_element(secondLevelMenu).perform()
        secondLevelMenu.click()

        product_code = self.browser.find_element_by_id("Prod")
        product_code.send_keys("RANDOM.AMS-value001")

        button_go = self.browser.find_element_by_id("btn_search_db")
        button_go.click()

        button_tech_properties = self.browser.find_element_by_id("getrecordRANDOM.AMS-value001")
        button_tech_properties.click()
        time.sleep(1)

        code = self.browser.find_element_by_xpath('//*[@id="testimonials"]/div[2]/div/div/table/tbody/tr/td[2]').text

        self.assertEquals(code, 'RANDOM.AMS-value001')