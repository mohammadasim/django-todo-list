from django import forms
from django.core.exceptions import ValidationError

from lists.models import Item, List

EMPTY_ITEM_ERROR = 'You cannot have an empty list item'
DUPLICATE_ITEM_ERROR = "You've already got this in your list"


class ItemForm(forms.models.ModelForm):
    """
    Form class for Items
    """

    class Meta:
        model = Item
        fields = ('text',)
        widgets = {
            'text': forms.fields.TextInput(attrs={
                'placeholder': 'Enter a to-do item',
                'class': 'form-control input-lg',
            })
        }
        error_messages = {
            'text': {'required': EMPTY_ITEM_ERROR}
        }


class NewListForm(ItemForm):

    def save(self, owner):
        if owner.is_authenticated:
            return List.create_new(first_item_text=self.cleaned_data['text'], owner=owner)
        else:
            return List.create_new(first_item_text=self.cleaned_data['text'])


class ExistingListItemForm(ItemForm):
    """
    Form class for adding items to an
    existing list
    """

    def __init__(self, for_list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.list = for_list

    def validate_unique(self):
        """
        Django uses a method called
        validate_unique both on forms
        and models and we can use
        both in conjunction with
        instance attribute.
        We have defined in the Item
        model that an item is unique
        in a list. In this method
        we override the form validate_unique()
        and call the model validate_unique()
        to test that the item being created
        is valid at the model level or not.
        """
        try:
            self.instance.validate_unique()
        except ValidationError as e:
            # We take validation error
            # adjust its error message
            # and then pass it back to
            # the form
            e.error_dict = {'text': [DUPLICATE_ITEM_ERROR]}
            self._update_errors(e)

    class Meta(ItemForm.Meta):
        pass
