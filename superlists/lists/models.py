from django.db import models


class List(models.Model):
    """
    Model representing a list.
    """
    pass


class Item(models.Model):
    """
    Model representing an item.
    """
    text = models.TextField('To-do list item')
    list = models.ForeignKey(List, on_delete=models.SET_DEFAULT, default=None)
