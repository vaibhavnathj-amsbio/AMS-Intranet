import time

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse

# from mixer.backend.django import mixer

from myDatabase.models import DataOwners


class TestmyDatabasePage(StaticLiveServerTestCase):
    databases = '__all__'

    def setUp(self):
        self.browser = webdriver.Chrome('./chromedriver.exe',)

    def tearDown(self):
        self.browser.close()

    def test_add_new_supplier_page(self):
        self.browser.maximize_window()
        self.browser.get(self.live_server_url)

        action = ActionChains(self.browser)

        firstLevelMenu = self.browser.find_element_by_id("database_drop_down")
        action.move_to_element(firstLevelMenu).perform()
        secondLevelMenu = self.browser.find_element_by_id("add_new_supplier")
        action.move_to_element(secondLevelMenu).perform()
        secondLevelMenu.click()

        comp_name = self.browser.find_element_by_id("comp_name")
        comp_name.send_keys("TESTNAME")

        acc_code = self.browser.find_element_by_id("acc_code")
        acc_code.send_keys("TESTCODE")

        dropdown = Select(self.browser.find_element_by_id("curr_code"))
        dropdown.select_by_visible_text("USD")

        button = self.browser.find_element_by_id("btn_submit")
        button.click()  # Send data to the database

        time.sleep(5)
        data_obj = DataOwners.objects.get(owner='TESTNAME')

        self.assertEquals(data_obj.dimmensionssuppliercode, "TESTCODE")
        self.assertEquals(data_obj.currencyid, 2)

    def test_search_db_page(self):
        self.browser.maximize_window()
        self.browser.get(self.live_server_url)

        action = ActionChains(self.browser)

        firstLevelMenu = self.browser.find_element_by_id("database_drop_down")
        action.move_to_element(firstLevelMenu).perform()
        secondLevelMenu = self.browser.find_element_by_id("search_db")
        action.move_to_element(secondLevelMenu).perform()
        secondLevelMenu.click()

        time.sleep(5)
        product_code = self.browser.find_element_by_id("Prod")
        product_code.send_keys("RANDOM.AMS-value001")

        button_go = self.browser.find_element_by_id("btn_search_db")
        button_go.click()
        time.sleep(5)

        button_tech_properties = self.browser.find_element_by_id(
            "getrecordRANDOM.AMS-value001")
        button_tech_properties.click()
        time.sleep(2)

        cat1 = self.browser.find_element_by_xpath('//*[@id="techRecordBodyAMS.MBS-K002-10mg Beads"]/tbody[1]/tr/td/label').text
        cat2 = self.browser.find_element_by_xpath('//*[@id="techRecordBodyAMS.MBS-K002-10mg Beads"]/tbody[3]/tr/td/label').text

        self.assertEquals(cat1, "Proteins & Peptides")
        self.assertEquals(cat2, "Molecular Biology")
