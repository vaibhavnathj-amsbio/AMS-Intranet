import time
from getpass import getuser

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
        ProductRecords.objects.create(product_code='RANDOM.AMS-value001', category_1=0)
        
    def tearDown(self):
        self.browser.close()

    def test_search_db_page(self):
        self.browser.maximize_window()
        self.browser.get(self.live_server_url)

        action = ActionChains(self.browser)

        firstLevelMenu = self.browser.find_element_by_id("database_drop_down")
        action.move_to_element(firstLevelMenu).perform()
        secondLevelMenu = self.browser.find_element_by_id("edit_single_product")
        action.move_to_element(secondLevelMenu).perform()
        secondLevelMenu.click()

        prod_code = self.browser.find_element_by_xpath('//*[@id="ProdCode"]')
        prod_code.send_keys('RANDOM.AMS-value001')

        submit_btn = self.browser.find_element_by_xpath('//*[@id="testimonials"]/div[1]/div/div/form/button')
        submit_btn.click()

        long_description = self.browser.find_element_by_xpath('//*[@id="id_long_description"]')
        long_description.send_keys('This is a very long description.')

        submit_form = self.browser.find_element_by_xpath('//*[@id="btnProdForm"]')
        submit_form.click()

        time.sleep(2)
        data_obj = ProductRecords.objects.get(pk='RANDOM.AMS-value001')

        self.assertEquals(data_obj.long_description, 'This is a very long description.')
        self.assertEquals(data_obj.last_updated_user, getuser().upper())



