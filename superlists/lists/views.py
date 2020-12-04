from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.views.generic import FormView
from django.views.generic import CreateView

from .forms import (ItemForm, ExistingListItemForm,
                    NewListForm, ListShareForm
                    )
from .models import Item, List

User = get_user_model()


class HopePageView(FormView):
    template_name = 'home.html'
    form_class = ItemForm


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
    list_share_form = ListShareForm(request.user)
    if request.method == 'POST':
        form = ExistingListItemForm(for_list=list_, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(list_)
        else:
            context = {
                'items': Item.objects.filter(list=list_),
                'form': form,
                'list': list_,
                'list_share_form': list_share_form
            }
            return render(request, 'list.html', context)
    if request.method == 'GET':
        items = Item.objects.filter(list=list_)
        context = {
            'items': items,
            'list': list_,
            'form': form,
            'list_share_form': list_share_form
        }
        return render(request, 'list.html', context)


def my_lists(request, email):
    owner = User.objects.get(email=email)
    context = {
        'owner': owner
    }
    return render(request, 'my_lists.html', context)


class NewListView(CreateView):
    template_name = 'home.html'
    form_class = NewListForm

    def form_valid(self, form):
        list_ = form.save(owner=self.request.user)
        return redirect(str(list_.get_absolute_url()))


def share_list(request, list_id):
    list_share_form = ListShareForm(request.user, data=request.POST)
    if list_share_form.is_valid():
        sharing_list = list_share_form.save(list_id)
        return redirect(str(sharing_list.get_absolute_url()))
    return render(request, 'list.html', {'list_share_form': list_share_form})
