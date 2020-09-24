import time
import os
from unittest import skip

from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException


class FunctionalTest(StaticLiveServerTestCase):
    """
    Test class containing test for
    new user functionality
    We have replaced LiverServerTestCase
    with StaticLiveServerTestCase so static
    files are loaded.
    """
    # The maximum amount of time we are prepared to wait
    Max_Wait = 10

    def setUp(self) -> None:
        """
        Setting up the browser
        :return:
        """
        self.browser = webdriver.Chrome()
        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url = 'http://' + staging_server

    def tearDown(self) -> None:
        """
        Tearing down the test setup
        :return:
        """
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        """
        Method to wait and check for items in a
        table row
        :param row_text:
        :return:
        """
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > self.Max_Wait:
                    raise e
                time.sleep(0.5)
