from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

from lists.models import Item, List

User = get_user_model()


class ItemModelTest(TestCase):

    def test_default_text(self):
        item = Item()
        self.assertEqual(item.text, '')

    def test_item_is_related_to_list(self):
        list_ = List.objects.create()
        item = Item()
        item.list = list_
        item.save()
        self.assertEqual(item, list_.item_set.all().first())

    def test_cannot_save_empty_list_items(self):
        list_ = List.objects.create()
        item = Item(list=list_, text='')
        """
        with statement is called context managers
        it wrap a block of code usually with some
        kind of setup, cleanup or error handling
        code.
        This is a new testing technique: when we
        want to check that doing something will
        raise an error, we can use self.assertRaise
        context manager.
        The text field in django model is set to 
        blank=false, yet we could create an item
        with blank text. This is because django
        model doesn't run full validation on save.
        Django does have a method to manually run
        full validation, its called full_clean.
        By running that method the problem is 
        identified and an assertion is raised.
        """
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()

    def test_duplicate_items_are_invalid(self):
        list_ = List.objects.create()
        Item.objects.create(list=list_, text='bla')
        with self.assertRaises(ValidationError):
            item = Item(list=list_, text='bla')
            item.full_clean()

    def test_can_save_item_to_different_lists(self):
        list1 = List.objects.create()
        list2 = List.objects.create()
        Item.objects.create(list=list1, text='bla')
        item = Item(list=list2, text='bla')
        item.full_clean()  # should not raise exception

    def test_list_ordering(self):
        list1 = List.objects.create()
        item1 = Item.objects.create(list=list1, text='i1')
        item2 = Item.objects.create(list=list1, text='item 2')
        item3 = Item.objects.create(list=list1, text='3')
        # We had to change queryset to list as even though
        # the result of the test was correct the queryset
        # and the list of items was the same, but still
        # the test was failing. Once we changed queryset
        # to a list, the test passed.
        self.assertEqual(list(Item.objects.all()),
                         [item1, item2, item3])

    def test_string_representation(self):
        item = Item(text='some text')
        self.assertEqual(str(item), 'some text')


class ListModelTest(TestCase):
    def test_get_absolute_url(self):
        list_ = List.objects.create()
        self.assertEqual(list_.get_absolute_url(), f'/lists/{list_.id}/')

    def test_create_new_creates_list_and_first_item(self):
        List.create_new(first_item_text='new item text')
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'new item text')
        new_list = List.objects.first()
        self.assertEqual(new_item.list, new_list)

    def test_create_new_optionally_saves_owner(self):
        user = User.objects.create()
        List.create_new(first_item_text='new item text', owner=user)
        new_list = List.objects.first()
        self.assertEqual(new_list.owner, user)

    # The following are sanity check tests
    # as List model will have user foreign key
    # as optional we are ensuring that having
    # a user and not having a user don't raise
    # any exceptions.

    def test_lists_can_have_owners(self):
        List(owner=User()) # should not raise

    def test_list_owner_is_optional(self):
        List().full_clean() # should not raise
        # full_clean() runs database level validation
        # checks on a model object.

    def test_create_new_returns_new_list_object(self):
        returned = List.create_new(first_item_text='new item text')
        new_list = List.objects.first()
        self.assertEqual(returned, new_list)

    def test_list_name_is_first_item_text(self):
        list_ = List.objects.create()
        Item.objects.create(text='first item', list=list_)
        Item.objects.create(text='second item', list=list_)
        self.assertEqual(list_.name, 'first item')

    def test_add_shared_with_method_adds_user_to_shared_with(self):
        list_owner = User.objects.create(email='a@b.com')
        shared_with_user = User.objects.create(email='b@b.com')
        test_list = List.objects.create(owner=list_owner)
        test_list.add_shared_with(shared_with_user.email)
        self.assertEqual(test_list.shared_with.all()[0].email, shared_with_user.email)

