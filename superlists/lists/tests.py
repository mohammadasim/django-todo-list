from django.http import HttpRequest
from django.test import TestCase, RequestFactory
from django.urls import resolve, reverse


class HomePageTest(TestCase):
    """
    Class to test the HomePageView
    """

    def setUp(self) -> None:
        url = reverse('home')
        self.response = self.client.get(url)

    def test_uses_home_template(self):
        self.assertTemplateUsed(self.response, 'home.html')

    def test_can_save_a_POST_request(self):
        response = self.client.post('/', data={
            'item_text': 'A new list item'
        })
        self.assertIn('A new list item', response.content.decode())
        self.assertTemplateUsed(response, 'home.html')
