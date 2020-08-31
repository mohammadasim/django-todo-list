from django.shortcuts import render, redirect
from .models import Item


def home_page(request):
    """
    Function based view for
    home page.
    :param request:
    :return:
    """
    if request.method == 'POST':
        new_item_text = request.POST.get('item_text')
        Item.objects.create(text=new_item_text)
        return redirect('/lists/the-only-list-in-the-world/')
    return render(request, 'home.html')


def view_list(request):
    """
    Function based view for
    individual lists
    :param request:
    :return:
    """
    items = Item.objects.all()
    return render(request, 'list.html',
                  {'items': items})
