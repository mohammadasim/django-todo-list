from django import forms

from lists.models import Item

EMPTY_ITEM_ERROR = 'You cannot have an empty list item'


class ItemForm(forms.models.ModelForm):
    """
    Form class for Items
    """
    def save(self, for_list):
        """
        overriding the save method.
        .instance attribute on a form
        represents the database object
        that is being modified or created.
        """
        self.instance.list = for_list
        return super().save()

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
