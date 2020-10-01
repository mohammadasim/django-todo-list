from django.test import TestCase
from django.core.exceptions import ValidationError

from lists.models import Item, List


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

    def test_CAN_save_item_to_different_lists(self):
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

