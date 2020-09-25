from django.test import TestCase
from django.core.exceptions import ValidationError

from lists.models import Item, List


class ListAndItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        list_ = List()
        list_.save()

        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.list = list_
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)
        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, 'Item the second')
        self.assertEqual(second_saved_item.list, list_)

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
