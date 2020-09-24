import time
import os
from unittest import skip

from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):
    @skip
    def test_cannot_add_empty_list_items(self):
        # Edith goes to the home page and accidentally tries
        # to submit an empty list item. She hits enter on
        # the empty input box.

        # The home page refreshes, and there is an error message
        # saying that list items cannot be empty.

        # She tries again with some test for the item, which now works.

        # Perversely, she now decides to submit a second blank list item

        # she receives a similar warning on the list page

        # And she can correct it by filling some text in
        self.fail('write me')
