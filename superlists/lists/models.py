from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

User = get_user_model()


class List(models.Model):
    """
    Model representing a list.
    """
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE)
    shared_with = models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name='list_shared')

    def get_absolute_url(self):
        return reverse(
            'view_list',
            args=[self.id]
        )

    @property
    def name(self):
        return self.item_set.first().text

    @classmethod
    def create_new(cls, *args, **kwargs):
        if kwargs.get('owner'):
            list_ = cls.objects.create(owner=kwargs.get('owner'))
        else:
            list_ = cls.objects.create()
        Item.objects.create(text=kwargs.get('first_item_text'), list=list_)
        return list_

    def add_shared_with(self, email):
        user_to_add = User.objects.get(email=email)
        self.shared_with.add(user_to_add)


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
