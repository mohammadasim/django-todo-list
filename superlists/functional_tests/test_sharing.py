from selenium import webdriver


from .test_my_lists import MyListsTest


def quit_if_possible(browser):
    try:
        browser.quit()
    except:
        pass


class SharingTest(MyListsTest):

    def test_can_share_a_list_with_another_user(self):
        # Edith is a logged in user
        self.create_pre_authenticated_session('edith@example.com')
        edith_browser = self.browser
        self.addCleanup(lambda: quit_if_possible(edith_browser))

        # Her friend oniciferous is also hanging out on the lists site
        oni_browser = webdriver.Chrome()
        self.addCleanup(lambda: quit_if_possible(oni_browser))
        self.browser = oni_browser
        self.create_pre_authenticated_session('oniciferous@example.com')

        # Edith goes to the home page and starts a list
        self.browser = edith_browser
        self.browser.get(self.live_server_url)
        self.add_list_item('Get help')

        # She notices a "share this list" option
        share_box = self.browser.find_element_by_css_selector(
            'input[name="share"]'
        )
        self.assertEqual(
            share_box.get_attribute('placeholder'),
            'your-friend@example.com'
        )


