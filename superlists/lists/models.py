from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse


class List(models.Model):
    """
    Model representing a list.
    """
    User = get_user_model()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    @property
    def name(self):
        return self.item_set.first().text

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

    def __str__(self):
        return self.text

    class Meta:
        ordering = ('id',)
        unique_together = ('list', 'text')
