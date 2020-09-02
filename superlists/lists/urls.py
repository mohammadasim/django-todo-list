from django.urls import path

from .views import (
    home_page,
    view_list,
    new_list,
    add_item)

urlpatterns = [
    path('', home_page, name='home'),
    path('lists/new', new_list, name='new_list'),
    path('lists/<int:list_id>/',
         view_list, name='view_list'),
    path('lists/<int:list_id>/add_item', add_item, name='add_item'),
]
