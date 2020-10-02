from django.shortcuts import render, redirect

from .forms import (ItemForm, ExistingListItemForm,
EMPTY_ITEM_ERROR, DUPLICATE_ITEM_ERROR
                    )
from .models import Item, List


def home_page(request):
    """
    Function based view for
    home page.
    :param request:
    :return:
    """
    return render(request, 'home.html', {'form': ItemForm()})


def view_list(request, list_id):
    """
    Function based view for
    individual lists
    :param list_id:
    :param request:
    :return:
    """
    list_ = List.objects.get(id=list_id)
    form = ExistingListItemForm(for_list=list_)
    if request.method == 'POST':
        form = ExistingListItemForm(for_list=list_, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(list_)
        else:
            context = {
                'items': Item.objects.filter(list=list_),
                'form': form,
                'list': list_
            }
            return render(request, 'list.html', context)
    if request.method == 'GET':
        items = Item.objects.filter(list=list_)
        context = {
            'items': items,
            'list': list_,
            'form': form
        }
        return render(request, 'list.html', context)


def new_list(request):
    form = ItemForm(data=request.POST)
    if form.is_valid():
        list_ = List.objects.create()
        form.save(for_list=list_)
        return redirect(list_)
    else:

        return render(request, 'home.html', {'form': form})
