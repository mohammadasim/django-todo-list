import time
import os
import sys
from datetime import datetime

from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException

# The maximum amount of time we are prepared to wait
Max_Wait = 10

# Setup required to run on the jenkins server
chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(chrome_options=chrome_options)

SCREEN_DUMP_LOCATION = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'screendumps'
)


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
        # Commented out as required for jenkins test run.
        # to run jenkins, the app needs to be deployed in
        # to a staging environment, which is not the case
        # with this app atm.
        # self.browser = driver
        self.browser = webdriver.Chrome()
        self.staging_server = os.environ.get('STAGING_SERVER')
        if self.staging_server:
            self.live_server_url = 'http://' + self.staging_server

    def tearDown(self) -> None:
        """
        Tearing down the test setup
        :return:
        """
        for _, err in self._outcome.errors:
            if err:
                if not os.path.exists(SCREEN_DUMP_LOCATION):
                    os.makedirs(SCREEN_DUMP_LOCATION)
                # We use enumerate to add a counter to the
                # browser windows.
                for ix, handle in enumerate(self.browser.window_handles):
                    # defining a new instance variable
                    self._windowid = ix
                    self.browser.switch_to.window(handle)
                    self.take_screenshot()
                    self.dump_html()
        self.browser.quit()
        super().tearDown()

    def take_screenshot(self):
        """
        Takes screenshots of the browser
        when tests fail
        """
        filename = self._get_filename() + '.png'
        print('screenshotting to ', filename)
        # Must use the full path in the filename
        # provided as the method argument
        self.browser.get_screenshot_as_file(filename)

    def dump_html(self):
        filename = self._get_filename() + '.html'
        print('dumping paget HTML to ', filename)
        with open(filename, 'w') as f:
            f.write(self.browser.page_source)

    def _get_filename(self):
        """
        Generates a unique filename, consisting of
        name of the test, the test class and a timestamp.
        """
        # time is set to ISO 8601 format, replacing : with . and
        # removing microseconds by limiting the length to index 19
        timestamp = datetime.now().isoformat().replace(':', '.')[:19]
        return '{folder}/{classname}.{method}-window{windowid}-{timestamp}'.format(
            folder=SCREEN_DUMP_LOCATION,
            classname=self.__class__.__name__,
            method=self._testMethodName,
            windowid=self._windowid,
            timestamp=timestamp
        )

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

    def add_list_item(self, item):
        self.get_item_input_box().send_keys(item)
        self.get_item_input_box().send_keys(Keys.ENTER)
