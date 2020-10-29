from unittest import skip

from django.conf import settings
from django.contrib.auth import BACKEND_SESSION_KEY, SESSION_KEY, get_user_model
from django.contrib.sessions.backends.db import SessionStore

from .base import FunctionalTest

User = get_user_model()


class MyListsTest(FunctionalTest):

    def create_pre_authenticated_session(self, email):
        """
        We create a session object in the database,the
        session key is the primary key of the user i-e email.
        We then add a cookie to the browser that matches the
        session on the server. On the next visit to the site
        the server should recognise us as a logged in user.
        """
        user = User.objects.create(email=email)
        session = SessionStore()
        session[SESSION_KEY] = user.pk
        session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
        session.save()
        # To set a cookie we need to first visit the domain.
        # 404 pages load the quickest
        self.browser.get(self.live_server_url + '/404_no_such_url')
        self.browser.add_cookie(
            dict(
                name=settings.SESSION_COOKIE_NAME,
                value=session.session_key,
                path='/',
            )
        )

    def test_logged_in_users_lists_are_save_as_my_lists(self):
        email = 'edith@example.com'
        self.browser.get(self.live_server_url)
        # ensure that she is not logged in
        self.wait_to_be_logged_out(email)

        # Edith is logged-in user
        self.create_pre_authenticated_session(email)
        self.browser.get(self.live_server_url)
        self.wait_to_be_logged_in(email)

    def test_logged_in_users_lists_are_save_as_my_lists(self):
        # Edith is a logged in user
        self.create_pre_authenticated_session('edith@example.com')
        self.browser.get(self.live_server_url)
        self.wait_to_be_logged_in('edith@example.com')

        # She goes to the home and starts a list
        self.add_list_item('Reticulate splines')
        self.add_list_item('Immanentize eschaton')
        first_list_url = self.browser.current_url

        # She notices a "My lists" link, for the first time
        self.browser.find_element_by_link_text('My lists').click()

        # She sees that her list is in there and named according to
        # its first list item
        self.wait_for(
            lambda: self.browser.find_element_by_link_text('Reticulate Splines')
        )
        self.browser.find_element_by_link_text('Reticulate splines').click()
        self.wait_for(
            lambda: self.assertEqual(self.browser.current_url, first_list_url))

        # She decides to start another list, just to see
        self.browser.get(self.live_server_url)
        self.add_list_item('Click cows')
        second_list_url = self.browser.current_url

        # Under 'my lists', her new list appears
        self.browser.find_element_by_link_text('My lists').click()
        self.wait_for(
            lambda: self.browser.find_element_by_link_text('Click cows')
        )
        self.browser.find_element_by_link_text('Click cows').click()
        self.wait_for(
            lambda: self.assertEqual(self.browser.current_url, second_list_url)
        )

        # She logs out. The 'My list' option disappears
        self.browser.find_element_by_link_text('Log out').click()
        self.wait_for(
            lambda: self.assertEqual(
                self.browser.find_element_by_link_text('My lists'), []
            )
        )