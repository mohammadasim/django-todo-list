import unittest

from django.contrib.auth import get_user_model
from django.forms import forms
from django.http import HttpRequest
from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.utils.html import escape
from unittest.mock import patch, Mock

from lists.forms import ItemForm, EMPTY_ITEM_ERROR, ExistingListItemForm, ListShareForm
from lists.models import Item, List
from lists.views import new_list, share_list

User = get_user_model()


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


class NewListViewIntegratedTest(TestCase):

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

    @unittest.skip
    @patch('lists.views.List')
    @patch('lists.views.ItemForm')
    def test_list_owner_is_saved_if_user_is_authenticated(
            self, mockItemFormClass, mockListClass):
        user = User.objects.create(email='a@b.com')
        self.client.force_login(user)

        mock_list = mockListClass.return_value

        def check_owner_assigned():
            self.assertEqual(mock_list.owner, user)

        mock_list.save.side_effect = check_owner_assigned

        self.client.post('/lists/new', data={'text': 'new item'})
        mock_list.save.assert_called_once_with()


@patch('lists.views.NewListForm')
class NewListViewUnitTest(unittest.TestCase):
    """
    The django TestCase class makes it too easy
    to write integrated tests. As a way of making
    sure, we are writing 'pure' isolated unit tests
    we will only use unittest.TestCase
    """

    def setUp(self):
        """
        We setup a basic POST request,
        building up the request by hand rather than
        using the (overlay integrated) Djanto Test Client.
        """
        self.request = HttpRequest()
        self.request.POST['text'] = 'new list item'
        self.request.user = Mock()

    def test_passes_POST_data_to_NewListForm(self, mockNewListForm):
        new_list(self.request)  # The view function is called
        mockNewListForm.assert_called_once_with(data=self.request.POST)

    def test_saves_form_with_owner_if_form_is_valid(self, mockNewListForm):
        mock_form = mockNewListForm.return_value  # ensure that the mock_form is a magic_mock object
        mock_form.is_valid.return_value = True  # ensure that the return value of the is_valid method is true
        new_list(self.request)
        mock_form.save.assert_called_once_with(owner=self.request.user)

    @patch('lists.views.redirect')
    def test_redirects_to_form_returned_object_if_form_valid(self,
                                                             mock_redirect, mockNewListForm):
        """
        Patch decorators are applied innermost first.
        So the redirect patch is applied before the newListForm
        which is a class level decorator.
        Therefore in the method arguments, mock_redirect should
        be before mockNewListForm.
        """
        mock_form = mockNewListForm.return_value
        mock_form.is_valid.return_value = True
        response = new_list(self.request)
        self.assertEqual(response, mock_redirect.return_value)

    @patch('lists.views.render')
    def test_renders_home_template_with_form_if_form_invalid(self,
                                                             mock_render, mockNewListForm):
        mock_form = mockNewListForm.return_value
        mock_form.is_valid.return_value = False

        response = new_list(self.request)
        self.assertEqual(response, mock_render.return_value)
        mock_render.assert_called_once_with(
            self.request, 'home.html', {'form': mock_form}
        )

    def test_does_not_save_if_form_invalid(self, mockNewListForm):
        mock_form = mockNewListForm.return_value
        mock_form.is_valid.return_value = False
        new_list(self.request)
        self.assertFalse(mock_form.save.called)


class MyListTest(TestCase):

    def test_my_lists_url_renders_my_lists_template(self):
        User.objects.create(email='a@b.com')
        response = self.client.get('/lists/users/a@b.com/')
        self.assertTemplateUsed(response, 'my_lists.html')

    def test_passes_correct_owner_to_the_template(self):
        User.objects.create(email='wrong_user@email.com')
        correct_user = User.objects.create(email='a@b.com')
        response = self.client.get('/lists/users/a@b.com/')
        self.assertEqual(response.context['owner'], correct_user)


class ShareListTest(TestCase):

    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.user = User.objects.create(email='a@b.com')
        self.shared_with_user = User.objects.create(email='b@b.com')

    def test_post_redirect_to_list_page(self):
        list_ = List.objects.create()
        request = self.factory.post(f'/lists/{list_.id}/share', data={'sharee': self.shared_with_user.email})
        request.user = self.user
        response = share_list(request, list_.id)
        self.assertEqual(response.url, f'/lists/{list_.id}/')
        self.assertEqual(response.status_code, 302)

    def test_post_add_user_to_shared_with(self):
        test_list = List.objects.create(owner=self.user)
        test_item = Item.objects.create(text='test text', list=test_list)
        self.client.post(f'/lists/{test_list.id}/share', data={'sharee': self.shared_with_user.email})
        self.assertIn(self.shared_with_user, test_list.shared_with.all())

    def test_post_empty_entry_raise_returns_list_page(self):
        test_list = List.objects.create(owner=self.user)
        response = self.client.post(f'/lists/{test_list.id}/share', data={'sharee': ''})
        self.assertTemplateUsed(response, 'list.html')

    def test_post_empty_entry_response_contains_list_share_form(self):
        test_list = List.objects.create(owner=self.user)
        response = self.client.post(f'/lists/{test_list.id}/share', data={'sharee': ''})
        self.assertIsInstance(response.context['list_share_form'], ListShareForm)


