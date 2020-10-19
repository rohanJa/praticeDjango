# importing 'decorators' for 'FBV' and 'Mixin' for 'CBV' in django

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView
from .models import RestaurantLocation
from .forms import RestaurantCreateForm, RestaurantLocationCreateForm
# Create your views here.

@login_required(login_url='/login/')
def restaurant_createview(request):
    form = RestaurantLocationCreateForm(request.POST or None)
    errors = None
    if form.is_valid():
        if request.user.is_authenticated():
            instance = form.save(commit=False)
            instance.owner = request.user
            instance.save()

            return HttpResponseRedirect('/restaurants/')
        else:
            return HttpResponseRedirect("/login/")
    if form.errors:
        errors = form.errors
    
    template_name = 'restaurants/form.html'

    context = {'form': form, 'errors': errors}
    return render(request, template_name, context)

'''
def restaurant_createview(request):
    template_name = 'restaurants/form.html'
    form = RestaurantCreateForm(request.POST or None) #remove extra line if the request is POST for filling the form
    errors = None

    if form.is_valid():
        obj = RestaurantLocation.objects.create(
                name = form.cleaned_data.get('name'),
                location = form.cleaned_data.get('location'),
                category = form.cleaned_data.get('category')
            )

        return HttpResponseRedirect('/restaurants/')

    if form.errors:
        errors = form.errors

    context = {"form": form, "errors": errors}
    return render(request, template_name, context)
'''

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
    # def get_context_data(self, *args,**kwargs):
    #     context = super(RestaurantDetailView, self).get_context_data(*args, **kwargs) 
    #     return context
    
    ''' 
        This object method will be invoked when their is parameter passed in 
        the "urls.py" and filter the object according to the category passed in the url
        url(r'^restaurants/(?P<slug>[\w-]+)/$',RestaurantDetailView.as_view()),
    '''
    # def get_object(self, *args, **kwargs):
    #     rest_id = self.kwargs.get('slug')
    #     obj =get_object_or_404(RestaurantLocation, slug__icontains=rest_id) # pk = rest_id
    #     print(obj)
    #     return obj


class RestaurantCreateView(LoginRequiredMixin, CreateView):
    form_class = RestaurantLocationCreateForm
    template_name = 'restaurants/form.html'
    success_url = '/restaurants/'
    login_url = '/login/'

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.owner = self.request.user

        return super(RestaurantCreateView, self).form_valid(form)