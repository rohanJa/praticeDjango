from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from .models import RestaurantLocation

# Create your views here.

class RestaurantListView(ListView):
    queryset=RestaurantLocation.objects.all()
    template_name='restaurants/restaurants_list.html'

class SearchRestaurantListView(ListView):
    template_name='restaurants/restaurants_list.html'
    
    def get_queryset(self):
        slug=self.kwargs.get('slug')
        if slug:
            # search for exact word or contains "substring" of the category not "subsequence" in the Database
            queryset = RestaurantLocation.objects.filter(
                    Q(category__iexact=slug) | 
                    Q(category__icontains=slug)
                )
        else:
            queryset=RestaurantLocation.objects.none()
        return queryset