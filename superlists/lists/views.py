from django.shortcuts import render, redirect
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
    Item.objects.create(text=request.POST['item_text'], list=list_)
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
