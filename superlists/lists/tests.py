from django.http import HttpRequest
from django.test import TestCase, RequestFactory
from django.urls import resolve, reverse
from .models import Item


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
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')


class ItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)
        self.assertEqual(saved_items[0].text, 'The first (ever) list item')
        self.assertEqual(saved_items[1].text, 'Item the second')

    def test_redirect_after_post(self):
        response = self.client.post('/', data={
            'item_text': 'A new list item'
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')

    def test_only_saves_items_when_necessary(self):
        self.client.get('/')
        self.assertEqual(Item.objects.count(), 0)

    def test_display_all_list_items(self):
        Item.objects.create(text='itemy 1')
        Item.objects.create(text='itemy 2')

        response = self.client.get('/')

        self.assertIn('itemy 1', response.content.decode())
        self.assertIn('itemy 2', response.content.decode())
