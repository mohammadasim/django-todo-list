import time
import os
from unittest import skip

from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException

# The maximum amount of time we are prepared to wait
Max_Wait = 10


def wait(fn):
    """
    Decorator function that will apply the wait
    logic to all the function in its argument.
    A decorator takes a function as an argument
    and modifies it.
    It is important that we add *args **kwargs
    as this allows the function that is to be
    decorated to have any number of args and
    kwargs.
    We have set a constant for max time.
    We then have an infinite loop with three
    ways to exit
    Either the elements are found, the assertion
    passes and we exit.
    Or we raise exception check that we haven't
    hit our time limit, if not we wait again by
    calling the sleep.
    If we hit our time limit we then raise an exception.
    """

    def modified_fun(*args, **kwargs):
        start_time = time.time()
        while True:
            try:
                return fn(*args, **kwargs)
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > Max_Wait:
                    raise e
                time.sleep(0.5)

    return modified_fun


class FunctionalTest(StaticLiveServerTestCase):
    """
    Test class containing test for
    new user functionality
    We have replaced LiverServerTestCase
    with StaticLiveServerTestCase so static
    files are loaded.
    """

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

    @wait
    def wait_for_row_in_list_table(self, row_text):
        """
        Method to wait and check for items in a
        table row
        :param row_text:
        :return:
        """

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    @wait
    def wait_for(self, fn):
        """
        Method to cause explicit wait.
        This method will be used to
        wait for page refresh in other
        test classes and methods.
        The method takes a function and
        we return the return value of the
        function.
        The function is a lambda function
        that checks to find an element in
        the page.
        as an argument
        :param fn:
        :return:
        """
        return fn()

    def get_item_input_box(self):
        return self.browser.find_element_by_id('id_text')

    def wait_to_be_logged_in(self, email):
        self.wait_for(lambda: self.browser.find_element_by_link_text('Log out'))
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertIn(email, navbar.text)

    def wait_to_be_logged_out(self, email):
        self.wait_for(lambda: self.browser.find_element_by_name('email'))
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertNotIn(email, navbar.text)
