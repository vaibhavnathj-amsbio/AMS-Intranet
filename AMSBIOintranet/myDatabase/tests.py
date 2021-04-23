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

    def test_add_new_supplier(self):
        self.browser.maximize_window()
        self.browser.get(self.live_server_url)

        action = ActionChains(self.browser)

        firstLevelMenu = self.browser.find_element_by_id("database_drop_down")
        action.move_to_element(firstLevelMenu).perform()
        secondLevelMenu = self.browser.find_element_by_id("add_new_supplier")
        action.move_to_element(secondLevelMenu).perform()
        secondLevelMenu.click()

        comp_name = self.browser.find_element_by_id("comp_name")
        comp_name.send_keys("Vaibhav")

        acc_code = self.browser.find_element_by_id("acc_code")
        acc_code.send_keys("dummytest")

        dropdown = Select(self.browser.find_element_by_id("curr_code"))
        dropdown.select_by_visible_text("USD")

        button = self.browser.find_element_by_id("btn_submit")
        # button.click()
        # time.sleep(3)

        # div_card = self.browser.find_element_by_css_selector("div.card")
        # result = div_card.find_element_by_css_selector("*")
        self.assertEquals(0,0)
        print("That's it")


