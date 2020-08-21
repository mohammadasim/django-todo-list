from django.http import HttpRequest
from django.test import TestCase
from django.urls import resolve

from .views import HomePageView


class HomePageTest(TestCase):
    """
    Class to test the HomePageView
    """

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEquals(found.func.__name__,
                          HomePageView.as_view().__name__)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = HomePageView.as_view()(request)
        html = response.content.decode('utf8')
        self.assertTrue(html.startswith('<html>'))
        self.assertIn('<title>To-Do lists</title>', html)
        self.assertTrue(html.endswith('</html>'))
