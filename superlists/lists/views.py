from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.utils.html import escape

from .models import Item, List


def home_page(request):
    """
    Function based view for
    home page.
    :param request:
    :return:
    """
    return render(request, 'home.html')


def view_list(request, list_id):
    """
    Function based view for
    individual lists
    :param list_id:
    :param request:
    :return:
    """
    list_ = List.objects.get(id=list_id)
    items = Item.objects.filter(list=list_)
    context = {
        'items': items,
        'list': list_
    }
    return render(request, 'list.html',
                  context)


def new_list(request):
    list_ = List.objects.create()
    item = Item(text=request.POST['item_text'], list=list_)
    try:
        item.full_clean()
        item.save()
    except ValidationError:
        list_.delete()
        error = escape('You cannot have an empty list item')
        return render(request, 'home.html', {'error': error})
    return redirect(f'/lists/{list_.id}/')


def add_item(request, list_id):
    """
    View function to add item to existing
    list
    :param request:
    :param list_id:
    :return:
    """
    existing_list = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST['item_text'], list=existing_list)
    return redirect(f'/lists/{existing_list.id}/')
