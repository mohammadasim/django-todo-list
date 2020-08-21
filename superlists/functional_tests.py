from selenium import webdriver
import unittest


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
        self.fail('Finish the test!')


# She is invited to enter a to-do item straight away.


# She types "Buy peacock feathers" into a text box

# When she hits enter, the page updates and now the page lists
# "1: Buy peacock feathers" as an item in a to-do list.


# There is still a text box inviting her to add another item.
# She enters "Use peacock feathers to make a fly"

# The page updates again, and now shows both items on her list.


# Edith wonders whether the site will remember her list. Then she
# sees that the site has generated a unique url for her -- there is some
# explanatory text to that effect.


# she visits that URL and her to-do list is still there.

# Satisfied, she goes back to sleep.

if __name__ == '__main__':
    unittest.main()
