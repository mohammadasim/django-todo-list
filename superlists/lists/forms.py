from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from lists.models import Item, List

EMPTY_ITEM_ERROR = 'You cannot have an empty list item'
DUPLICATE_ITEM_ERROR = "You've already got this in your list"

User = get_user_model()


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


class ListShareForm(forms.Form):
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    sharee = forms.EmailField(required=True, label='Share this list',
                              widget=forms.EmailInput(
                                  attrs=
                                  {
                                      'placeholder': 'your-friend@example.com'
                                  }
                              ))

    def clean_sharee(self):
        shared_with_user_email = self.cleaned_data['sharee']
        shared_with_user = User.objects.filter(email=shared_with_user_email)
        if shared_with_user.exists():
            if shared_with_user[0] == self.user:
                raise forms.ValidationError(
                    'User cannot share list with itself.'
                )
            return shared_with_user_email
        raise forms.ValidationError(
            f'User {shared_with_user_email} is not a registered user.'
        )

    def save(self, list_id):
        sharing_list = List.objects.get(id=list_id)
        sharing_list.add_shared_with(email=self.cleaned_data['sharee'])
        return sharing_list
