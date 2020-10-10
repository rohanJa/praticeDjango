from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView
from .models import RestaurantLocation

# Create your views here.

class RestaurantListView(ListView):

    def get_queryset(self):
        slug=self.kwargs.get('slug')
        if slug:
            # search for exact word or contains "substring" of the category not "subsequence" in the Database
            queryset = RestaurantLocation.objects.filter(
                    Q(category__iexact=slug) | 
                    Q(category__icontains=slug)
                )
        else:
            # return list of all restaurant in the DB if category is not specified in url 
            queryset = RestaurantLocation.objects.all()

        return queryset    

class RestaurantDetailView(DetailView):
    queryset = RestaurantLocation.objects.all()

    def get_context_data(self, *args,**kwargs):
        context = super(RestaurantDetailView, self).get_context_data(*args, **kwargs) 
        return context
    
    def get_object(self, *args, **kwargs):
        rest_id = self.kwargs.get('rest_id')
        obj =get_object_or_404(RestaurantLocation, id=rest_id) # pk = rest_id
        return obj