from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect

from .forms import (ItemForm, ExistingListItemForm,
                    NewListForm
                    )
from .models import Item, List

User = get_user_model()


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


def my_lists(request, email):
    owner = User.objects.get(email=email)
    context = {
        'owner': owner
    }
    return render(request, 'my_lists.html', context)


def new_list(request):
    form = NewListForm(data=request.POST)
    if form.is_valid():
        list_ = form.save(owner=request.user)
        return redirect(str(list_.get_absolute_url()))
    else:
        return render(request, 'home.html', {'form': form})
