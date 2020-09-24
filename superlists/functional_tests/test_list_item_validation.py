import time
import os
from unittest import skip

from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_list_items(self):
        # Edith goes to the home page and accidentally tries
        # to submit an empty list item. She hits enter on
        # the empty input box.
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)

        # The home page refreshes, and there is an error message
        # saying that list items cannot be empty.
        """
        We call the wiat_for method and pass it a lambda function
        the lambda function checks if the page has a the specified
        css selector and returns true or false.
        Based on this return value value the loop in the wait_for
        method will be broken.
        """
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector('.has-error').text,
            "You can't have an empty list item."
        ))

        # She tries again with some test for the item, which now works.
        self.browser.find_element_by_id('id_new_item').send_keys('Buy milk')
        self.browser.find_element_by_id('id_new_item').send_keys('Keys.ENTER')
        self.wait_for_row_in_list_table('1: Buy milk')

        # Perversely, she now decides to submit a second blank list item
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)

        # she receives a similar warning on the list page
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector('.has-error').text,
            "You can't have an empty list item."
        ))

        # And she can correct it by filling some text in
        self.browser.find_element_by_id('id_new_item').send_keys('Make tea')
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')
        self.wait_for_row_in_list_table('2: Make tea')
