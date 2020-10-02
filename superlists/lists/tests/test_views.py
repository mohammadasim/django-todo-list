from unittest import skip

from django.test import TestCase
from django.urls import reverse
from django.utils.html import escape

from lists.forms import ItemForm, EMPTY_ITEM_ERROR, ExistingListItemForm
from lists.models import Item, List


class HomePageTest(TestCase):
    """
    Class to test the HomePageView
    """

    def setUp(self) -> None:
        url = reverse('home')
        self.response = self.client.get(url)

    def test_uses_home_template(self):
        self.assertTemplateUsed(self.response, 'home.html')

    def test_home_page_uses_item_form(self):
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], ItemForm)


class ListViewTest(TestCase):
    """
    Class to test ListView
    """

    def test_display_item_form(self):
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')
        self.assertIsInstance(response.context['form'], ExistingListItemForm)
        self.assertContains(response, 'name="text"')

    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text='itemy 1', list=correct_list)
        Item.objects.create(text='itemy 2', list=correct_list)

        other_list = List.objects.create()
        Item.objects.create(text='other list item 1', list=other_list)
        Item.objects.create(text='other list item 2', list=other_list)

        response = self.client.get(f'/lists/{correct_list.id}/')
        self.assertContains(response, 'itemy 1')
        self.assertContains(response, 'itemy 2')
        self.assertNotContains(response, 'other list item 1')
        self.assertNotContains(response, 'other list item 2')

    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get(f'/lists/{correct_list.id}/')
        self.assertEqual(response.context['list'], correct_list)

    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        self.client.post(
            f'/lists/{correct_list.id}/',
            data={'text': 'A new item for an existing list'}
        )
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, correct_list)

    def test_POST_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            f'/lists/{correct_list.id}/',
            data={'text': 'A new item for an existing list'}
        )
        self.assertRedirects(
            response, f'/lists/{correct_list.id}/'
        )

    def test_validation_errors_end_up_on_list_page(self):
        list_ = List.objects.create()
        response = self.client.post(
            f'/lists/{list_.id}/',
            data={'text': ''}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list.html')
        expected_error = 'You cannot have an empty list item'
        self.assertContains(response, expected_error)

    def test_duplicate_item_validation_errors_end_up_on_lists_page(self):
        list1 = List.objects.create()
        item1 = Item.objects.create(list=list1, text='textey')
        response = self.client.post(
            f'/lists/{list1.id}/',
            data={'text': 'textey'}
        )
        expected_error = escape("You've already got this in your list")
        self.assertContains(response, expected_error)
        self.assertTemplateUsed(response, 'list.html')
        self.assertEqual(Item.objects.all().count(), 1)

    def test_for_invalid_input_passes_to_existing_list_passes_ExistingListItemForm(self):
        list_ = List.objects.create()
        Item.objects.create(list=list_, text='Hello world')
        response = self.client.post(
            f'/lists/{list_.id}/',
            data={'text': 'Hello world'}
        )
        self.assertIsInstance(response.context['form'], ExistingListItemForm)


class NewListTest(TestCase):
    def post_invalid_input_new_list(self):
        return self.client.post('/lists/new', data={'text': ''})

    def test_can_save_a_POST_request(self):
        response = self.client.post('/lists/new', data={
            'text': 'A new list item'
        })
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirect_after_post(self):
        response = self.client.post('/lists/new', data={
            'text': 'A new list item'
        })
        new_list = List.objects.first()
        self.assertRedirects(response, f'/lists/{new_list.id}/')

    def test_validation_errors_are_sent_back_to_home_page_template(self):
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        expected_error = 'You cannot have an empty list item'
        self.assertContains(response, expected_error)

    def test_invalid_list_items_arent_saved(self):
        self.client.post('/lists/new', data={'text': ''})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)

    def test_for_invalid_input_passes_form_to_template(self):
        response = self.post_invalid_input_new_list()
        self.assertIsInstance(response.context['form'], ItemForm)

    def test_validation_errors_are_shown_on_home_page(self):
        response = self.post_invalid_input_new_list()
        self.assertContains(response, EMPTY_ITEM_ERROR)

    def test_for_invalid_input_renders_home_template(self):
        response = self.post_invalid_input_new_list()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
