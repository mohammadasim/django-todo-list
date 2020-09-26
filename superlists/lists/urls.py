
from django.urls import path
from .views import (
    home_page,
    view_list,
    new_list,)

urlpatterns = [
    path('new', new_list, name='new_list'),
    path('<int:list_id>/', view_list, name='view_list'),
]
