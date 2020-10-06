from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
# function based views

def home(request):

    return render(request,"base.html", {"html_var":"AJJU"})