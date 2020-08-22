from django.http import HttpRequest
from django.test import TestCase, RequestFactory
from django.urls import resolve, reverse

from .views import HomePageView


class HomePageTest(TestCase):
    """
    Class to test the HomePageView
    """
    def setUp(self) -> None:
        url = reverse('home')
        self.response = self.client.get(url)

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEquals(found.func.__name__,
                          HomePageView.as_view().__name__)

    def test_uses_home_template(self):
        self.assertTemplateUsed(self.response, 'home.html')
