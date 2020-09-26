from django.db import models
from django.urls import reverse


class List(models.Model):
    """
    Model representing a list.
    """
    def get_absolute_url(self):
        return reverse(
            'view_list',
            args=[self.id]
        )


class Item(models.Model):
    """
    Model representing an item.
    """
    text = models.TextField('To-do list item')
    list = models.ForeignKey(List, on_delete=models.SET_DEFAULT, default=None)
