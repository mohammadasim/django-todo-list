from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView


class HomePageView(TemplateView):

    def get(self, request, *args, **kwargs):
        return HttpResponse('<html><title>To-Do lists</title></html>')
