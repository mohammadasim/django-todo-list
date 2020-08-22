import time

from selenium import webdriver
import unittest

from selenium.webdriver.common.keys import Keys


class NewVisitorTest(unittest.TestCase):
    """
    Test class containing test for
    new user functionality
    """

    def setUp(self) -> None:
        """
        Setting up the browser
        :return:
        """
        self.browser = webdriver.Chrome()

    def tearDown(self) -> None:
        """
        Tearing down the test setup
        :return:
        """
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Edith has heard about a cool new online to-do app. She goes
        # to check out its home page.
        self.browser.get('http://127.0.0.1:8000')

        # She notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # She is invited to enter a to-do item straight away.
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # She types "Buy peacock feathers" into a text box
        inputbox.send_keys('Buy peacock feathers')

        # When she hits enter, the page updates and now the page lists
        # "1: Buy peacock feathers" as an item in a to-do list.
        inputbox.send_keys(Keys.Enter)
        time.sleep(1)
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(
            any(row.text == '1: Buy feathers' for row in rows)
        )

        # There is still a text box inviting her to add another item.
        # She enters "Use peacock feathers to make a fly"
        self.fail('Finish the test!')


# The page updates again, and now shows both items on her list.


# Edith wonders whether the site will remember her list. Then she
# sees that the site has generated a unique url for her -- there is some
# explanatory text to that effect.


# she visits that URL and her to-do list is still there.

# Satisfied, she goes back to sleep.

if __name__ == '__main__':
    unittest.main()
