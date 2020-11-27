"""
Module to test Item form class
"""
import unittest
from unittest.mock import patch, Mock

from django.contrib.auth import get_user_model
from django.test import TestCase

from lists.forms import (EMPTY_ITEM_ERROR, DUPLICATE_ITEM_ERROR,
                         ItemForm, ExistingListItemForm, NewListForm,
                         ListShareForm,
                         )
from lists.models import List, Item

User = get_user_model()


class ItemFormTest(TestCase):
    """
    Class containing tests methods
    for ItemForm
    """

    def test_form_renders_item_text_input(self):
        form = ItemForm()
        self.assertIn('placeholder="Enter a to-do item"', form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())

    def test_form_validation_for_blank_items(self):
        form = ItemForm(data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['text'],
            [EMPTY_ITEM_ERROR]
        )


class ExistingListItemFormTest(TestCase):

    def test_form_renders_item_text_input(self):
        list_ = List.objects.create()
        form = ExistingListItemForm(for_list=list_)
        self.assertIn('placeholder="Enter a to-do item"', form.as_p())

    def test_form_validation_for_blank_items(self):
        list_ = List.objects.create()
        form = ExistingListItemForm(for_list=list_, data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [EMPTY_ITEM_ERROR])

    def test_form_validation_for_duplicate_items(self):
        list_ = List.objects.create()
        Item.objects.create(list=list_, text='no twins!')
        form = ExistingListItemForm(for_list=list_, data={'text': 'no twins!'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [DUPLICATE_ITEM_ERROR])

    def test_form_save(self):
        list_ = List.objects.create()
        form = ExistingListItemForm(for_list=list_, data={'text': 'hi'})
        new_item = form.save()
        self.assertEqual(new_item, Item.objects.all()[0])


class NewListFormTest(unittest.TestCase):

    @patch('lists.forms.List.create_new')
    def test_save_creates_new_list_from_post_data_if_user_not_authenticated(self,
                                                                            mock_list_create_new):
        user = Mock(is_authenticated=False)
        form = NewListForm(data={'text': 'new item text'})
        form.is_valid()
        form.save(user)
        mock_list_create_new.assert_called_once_with(
            first_item_text='new item text'
        )

    @patch('lists.forms.List.create_new')
    def test_save_creates_new_list_with_owner_if_user_authenticated(
            self, mock_list_create_new):
        user = Mock(is_authenticated=True)
        form = NewListForm(data={'text': 'new item text'})
        form.is_valid()
        form.save(user)
        mock_list_create_new.assert_called_once_with(
            first_item_text='new item text', owner=user
        )

    @patch('lists.forms.List.create_new')
    def test_save_returns_new_list_object(
            self, mock_list_create_new):
        user = Mock(is_authenticated=True)
        form = NewListForm(data={'text': 'new item text'})
        form.is_valid()
        response = form.save(owner=user)
        self.assertEqual(response, mock_list_create_new.return_value)


class ListShareFormTest(unittest.TestCase):
    def setUp(self):
        self.test_user = User.objects.create(email='a@z.com')

    def test_form_renders_email_input_item(self):
        form = ListShareForm(self.test_user)
        self.assertIn('type="email"', form.as_p())
        self.assertIn('placeholder="your-friend@example.com"', form.as_p())

    def test_form_validation_for_blank_email_field(self):
        form = ListShareForm(self.test_user, data={'email': ''})
        self.assertFalse(form.is_valid())

    def test_form_validation_for_non_existing_user(self):
        form = ListShareForm(self.test_user, data={'email': 'c@b.com'})
        self.assertFalse(form.is_valid())

    def test_form_validation_for_sharing_list_with_list_owner(self):
        form = ListShareForm(self.test_user, data={'email': self.test_user.email})
        self.assertFalse(form.is_valid())

    def test_form_saves_valid_data(self):
        shared_with_user = User.objects.create(email='test@email.com')
        test_list = List.objects.create(owner=self.test_user)
        form = ListShareForm(self.test_user, data={'email': shared_with_user.email})
        self.assertTrue(form.is_valid())
